import logging
import numpy as np
import torch
import os
import json
import wandb
from torch.utils.data import DataLoader


from . import params


def generation(model, wandb_run, logger: logging.Logger):
    from .functional import generate

    logger.info('Generating Samples from Prior')
    outputs = generate(model, logger)
    for temp_i, temp_outputs in enumerate(outputs):
        samples = []
        for sample_i, output in enumerate(temp_outputs):
            sample = wandb.Image(output, caption=f'Prior sample {sample_i}')
            samples.append(sample)
        wandb_run.log({f"generation {temp_i}": samples}, step=temp_i)
    logger.info(f'Generation successful')


def mei(model, wandb_run, logger: logging.Logger):
    logger.info('Generating Most Exciting Inputs (MEI)')
    for op_name, op in params.analysis_params.mei.items():
        result = generate_mei(model, op["objective"], op["use_mean"],
                              op["type"], op["config"])
        vis = result.get_image().detach().cpu().numpy()
        for i, image in enumerate(vis):
            wandb_run.log(
                {f"MEI {op_name}": wandb.Image(image)}, step=i
            )
    logger.info(f'MEI generation successful')


def generate_mei(model, objective, use_mean, mei_type, mei_config):
    from meitorch.mei import MEI

    def operation(inputs):
        computed, _ = model(inputs, use_mean=use_mean)
        objective_result = objective(computed)
        if isinstance(objective_result, torch.Tensor):
            return dict(objective=-objective_result,
                        activation=objective_result)
        elif isinstance(objective_result, dict):
            assert 'objective' in objective_result and 'activation' in objective_result, \
                'objective_result must contain keys "objective" and "activation"'
            return objective_result
    mei_object = MEI(operation=operation, shape=params.data_params.shape)

    if mei_type == 'pixel':
        results = mei_object.generate_pixel_mei(**mei_config)
    elif mei_type == 'distribution':
        results = mei_object.generate_variational_mei(**mei_config)
    elif mei_type == 'transform':
        results = mei_object.generate_transformation_based(**mei_config)
    else:
        raise ValueError(f'Unknown MEI type {mei_type}')
    return results


def white_noise_analysis(model, wandb_run, logger: logging.Logger):
    logger.info('Generating Samples with White Noise Analysis')
    shape = params.data_params.shape
    for target_block, config in params.analysis_params.white_noise_analysis.items():
        n_samples = config['n_samples']
        sigma = config['sigma']
        receptive_fields = \
            generate_white_noise_analysis(model, target_block, shape, n_samples, sigma)
        n_dims = receptive_fields.shape[0]

        for i in range(n_dims):
            rf = receptive_fields[i, :].reshape(shape)
            wandb_run.log(
                {f"white noise analysis {target_block}": wandb.Image(rf)}, step=i
            )


def generate_white_noise_analysis(model, target_block, shape, n_samples=100, sigma=0.6):
    import scipy

    if shape[0] == 1:
        shape = shape[1:]
    white_noise = np.random.normal(size=(n_samples, np.prod(shape)), loc=0.0, scale=1.).astype(np.float32)

    # apply ndimage.gaussian_filter with sigma=0.6
    for i in range(n_samples):
        white_noise[i, :] = scipy.ndimage.gaussian_filter(
            white_noise[i, :].reshape(shape), sigma=sigma).reshape(np.prod(shape))

    computed, _ = model(torch.ones(1, *shape), stop_at=target_block)
    target_block_dim = computed[target_block].shape[1:]
    target_block_values = np.zeros((n_samples, *target_block_dim), dtype=np.float32)

    # loop over a batch of 128 white_noise images
    for i in range(0, n_samples, 128):
        batch = white_noise[i:i+128, :]
        computed_target, _ = model(torch.from_numpy(batch), use_mean=True, stop_at=target_block)
        target_block_values[i:i+128, :] = computed_target[target_block].detach().numpy()

    # multiply transpose of target block_values with white noise tensorially
    receptive_fields = np.matmul(target_block_values.transpose(), white_noise) / np.sqrt(n_samples)
    return receptive_fields


def decodability(model, labeled_loader, wandb_run, logger: logging.Logger):
    logger.info('Computing Decodability')
    results = calculate_decodability(model, labeled_loader)
    accuracies = {decode_from: accuracy for decode_from, (_, accuracy) in results.items()}
    for decode_from, (loss_history, accuracy) in results.items():
        # loss history -> line plot
        data = [[x, y] for (x, y) in enumerate(loss_history)]
        table = wandb.Table(data=data, columns=["step", "loss"])
        wandb_run.log({"decodability_loss_history":
                      wandb.plot.line(table, "step", "loss",
                                      title=f"Decodability Loss History {decode_from}")})

    # accuracy -> bar plot
    data = [[decode_from, acc] for (decode_from, acc) in accuracies.items()]
    table = wandb.Table(data=data, columns =["decode_from", "accuracy"])
    wandb_run.log({"decodability_accuracies":
                   wandb.plot.bar(table, "decode_from", "accuracy",
                                  title="Deocdability Accuracies")})
    logger.info(f'Decodability calculation successful')


def calculate_decodability(model, labeled_loader):
    from .elements.dataset import FunctionalDataset

    decode_from_list = params.analysis_params.decodability.keys()
    X = {layer: [] for layer in decode_from_list}
    Y = []
    for batch in labeled_loader:
        inputs, labels = batch
        computed, _ = model(inputs, use_mean=True)
        for decode_from in decode_from_list:
            X[decode_from].append(
                computed[decode_from].numpy())
            Y.append(labels)
    X = {block: np.concatenate(block_inputs, axis=0)
         for block, block_inputs in X.items()}
    Y = np.concatenate(Y, axis=0)

    results = dict()
    for decode_from in decode_from_list:
        decoder_model = params.analysis_params.decodability[decode_from]["model"]()
        decoding_dataset = FunctionalDataset(data=X[decode_from], labels=Y)
        optimizer = params.analysis_params.decodability[decode_from]["optimizer"](
            decoder_model.parameters(),
            lr=params.analysis_params.decodability[decode_from]["learning_rate"])
        loss = params.analysis_params.decodability[decode_from]["loss"]()
        loss_history, accuracy = train_decoder(
            decoder_model, optimizer, loss, params.analysis_params.decodability[decode_from]["epochs"],
            params.analysis_params.decodability[decode_from]["batch_size"], decoding_dataset)
        results[decode_from] = (loss_history, accuracy)
    return results


def train_decoder(decoder_model, optimizer, loss, epochs, batch_size, dataset):
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    loss_history = []
    # train model
    for epoch in range(epochs):
        for batch in dataloader:
            X, Y = batch
            optimizer.zero_grad()
            output = decoder_model(X)
            batch_loss = loss(output, Y)
            loss_history.append(batch_loss.item())
            batch_loss.backward()
            optimizer.step()

    # evaluate model
    # TODO: add evaluation -> calcualte accuracy
    return loss_history, 0


def latent_step_analysis(model, dataloader, wandb_run, logger: logging.Logger):
    """
    logger.info('Generating Images with Latent Step Analysis')
    traversal_folder = os.path.join(save_path, 'latent_step_analysis')
    os.makedirs(traversal_folder, exist_ok=True)
    sample = next(iter(dataloader))
    for target_block, config in get_hparams().analysis_params.latent_step.queries.items():
        latent_step_analysis(model, sample, target_block, traversal_folder, **config)
    logger.info(f'Latent Traversal Images saved to {traversal_folder}')
    """
    raise NotImplementedError()

"""
def latent_step_analysis(model, sample, target_block, save_path, n_cols=10, diff=1, value=1, n_dims=70):
    compute_target_block = model.compute_function(target_block)
    target_computed, _ = compute_target_block(sample)
    input_0 = target_computed[target_block]

    compute_output = model.compute_function('output')
    output_computed, _ = compute_output(target_computed, use_mean=True)
    output_0 = torch.mean(output_computed['output'], dim=0)

    n_rows = int(np.ceil(n_dims / n_cols))
    fig, ax = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=(n_cols * 2, n_rows * 2))

    for i in range(n_dims):
        input_i = np.zeros([1, n_dims])
        input_i[0, i] = value
        input_i = input_0 + input_i
        target_computed[target_block] = input_i

        trav_output_computed, _ = compute_output(target_computed, use_mean=True)
        output_i = torch.mean(trav_output_computed, dim=0)

        ax[i // n_cols][i % n_cols].imshow(output_i - diff * output_0, interpolation='none', cmap='gray')
        ax[i // n_cols][i % n_cols].set_title(f"{i}")
        ax[i // n_cols][i % n_cols].axis('off')

    path = os.path.join(save_path, f"{target_block}_trav.png")
    plt.title(f"{target_block} traversal")
    fig.savefig(path, facecolor="white")
"""


