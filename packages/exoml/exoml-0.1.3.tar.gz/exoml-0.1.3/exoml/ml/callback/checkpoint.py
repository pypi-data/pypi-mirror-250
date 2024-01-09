import logging
import os.path
import shutil

from keras.callbacks import ModelCheckpoint
from keras.utils import tf_utils, io_utils


class ModelCheckpointCallback(ModelCheckpoint):
    def __init__(self, filepath, original_path, monitor: str = "val_loss", verbose: int = 0,
                 save_best_only: bool = False,
                 save_weights_only: bool = False, mode: str = "auto", save_freq="epoch", options=None,
                 initial_value_threshold=None, **kwargs):
        super().__init__(filepath, monitor, verbose, save_best_only, save_weights_only, mode, save_freq, options,
                         initial_value_threshold, **kwargs)
        self.original_path = original_path

    def on_epoch_end(self, epoch, logs=None):
        self.epochs_since_last_save += 1
        if self.save_freq == "epoch":
            self._save_model(epoch=epoch, batch=None, logs=logs)

    def copy_files(self):
        if os.path.exists(self.original_path + '/training_log.csv'):
            shutil.copyfile(self.original_path + '/training_log.csv', self.filepath + '/training_log.csv')
        if os.path.exists(self.original_path + '/train_dataset.csv'):
            shutil.copyfile(self.original_path + '/train_dataset.csv', self.filepath + '/train_dataset.csv')
        if os.path.exists(self.original_path + '/validation_dataset.csv'):
            shutil.copyfile(self.original_path + '/validation_dataset.csv', self.filepath + '/validation_dataset.csv')
        if os.path.exists(self.original_path + '/network.png'):
            shutil.copyfile(self.original_path + '/network.png', self.filepath + '/network.png')
        if os.path.exists(self.original_path + '/metrics.png'):
            shutil.copyfile(self.original_path + '/metrics.png', self.filepath + '/metrics.png')

    def _save_model(self, epoch, batch, logs):
        """Saves the model.

        Args:
            epoch: the epoch this iteration is in.
            batch: the batch this iteration is in. `None` if the `save_freq`
              is set to `epoch`.
            logs: the `logs` dict passed in to `on_batch_end` or `on_epoch_end`.
        """
        logs = logs or {}

        if (
                isinstance(self.save_freq, int)
                or self.epochs_since_last_save >= self.period
        ):
            # Block only when saving interval is reached.
            logs = tf_utils.sync_to_numpy_or_python_type(logs)
            self.epochs_since_last_save = 0
            filepath = self._get_file_path(epoch, batch, logs)

            try:
                if self.save_best_only:
                    current = logs.get(self.monitor)
                    if current is None:
                        logging.warning(
                            "Can save best model only with %s available, "
                            "skipping.",
                            self.monitor,
                        )
                    else:
                        if self.monitor_op(current, self.best):
                            if self.verbose > 0:
                                io_utils.print_msg(
                                    f"\nEpoch {epoch + 1}: {self.monitor} "
                                    "improved "
                                    f"from {self.best:.5f} to {current:.5f}, "
                                    f"saving model to {filepath}"
                                )
                            self.best = current
                            if self.save_weights_only:
                                self.model.save_weights(
                                    filepath,
                                    overwrite=True,
                                    options=self._options,
                                )
                            else:
                                self.model.save(
                                    filepath,
                                    overwrite=True,
                                    options=self._options,
                                )
                            self.copy_files()
                        else:
                            if self.verbose > 0:
                                io_utils.print_msg(
                                    f"\nEpoch {epoch + 1}: "
                                    f"{self.monitor} did not improve "
                                    f"from {self.best:.5f}"
                                )
                else:
                    if self.verbose > 0:
                        io_utils.print_msg(
                            f"\nEpoch {epoch + 1}: saving model to {filepath}"
                        )
                    if self.save_weights_only:
                        self.model.save_weights(
                            filepath, overwrite=True, options=self._options
                        )
                    else:
                        self.model.save(
                            filepath, overwrite=True, options=self._options
                        )
                    self.copy_files()
                self._maybe_remove_file()
            except IsADirectoryError:  # h5py 3.x
                raise IOError(
                    "Please specify a non-directory filepath for "
                    "ModelCheckpoint. Filepath used is an existing "
                    f"directory: {filepath}"
                )
            except IOError as e:  # h5py 2.x
                # `e.errno` appears to be `None` so checking the content of
                # `e.args[0]`.
                if "is a directory" in str(e.args[0]).lower():
                    raise IOError(
                        "Please specify a non-directory filepath for "
                        "ModelCheckpoint. Filepath used is an existing "
                        f"directory: f{filepath}"
                    )
                # Re-throw the error for any other causes.
                raise e
