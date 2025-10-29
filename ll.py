"""
AI Trainer GUI — TensorFlow + PyTorch + PyQt5
Fichier unique: ai_gui_full.py
Fonctionnalités ajoutées :
- Choix de dataset: synthétique (make_classification) ou MNIST (téléchargement automatique)
- Entraînement TF et PyTorch dans des QThreads
- Sauvegarde / chargement des modèles (TF: model.save / model = tf.keras.models.load_model ; Torch: torch.save / torch.load)
- Affichage d'images (MNIST) et prédictions en temps réel
- Tracé des courbes loss/accuracy avec matplotlib intégré à PyQt5
- Options pour ajuster hyperparamètres (epochs, batch size, lr)
- Logs et gestion d'erreurs

Remarque : installe les dépendances :
pip install pyqt5 numpy scikit-learn matplotlib tensorflow torch torchvision

Lance: python ai_gui_full.py
"""

import sys
import os
import time
import traceback
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# PyQt5
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit,
    QProgressBar, QLabel, QHBoxLayout, QMessageBox, QComboBox,
    QSpinBox, QDoubleSpinBox, QFileDialog, QGridLayout, QListWidget,
    QGroupBox
)
from PyQt5.QtCore import QThread, pyqtSignal, Qt

# Matplotlib for plotting inside PyQt5
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# TensorFlow & PyTorch
import tensorflow as tf
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader

# Optional torchvision for MNIST transforms (only for PyTorch loader)
from torchvision import datasets, transforms

# -----------------------
# Utilities & Data
# -----------------------

def generate_synthetic(n_samples=2000, n_features=20, n_informative=10, random_state=1):
    X, y = make_classification(
        n_samples=n_samples,
        n_features=n_features,
        n_informative=n_informative,
        n_redundant=0,
        n_classes=2,
        random_state=random_state
    )
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=random_state
    )
    return X_train.astype(np.float32), X_test.astype(np.float32), y_train.astype(np.int64), y_test.astype(np.int64)


def load_mnist_for_tf():
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
    # normalize and reshape
    x_train = x_train.astype('float32') / 255.0
    x_test = x_test.astype('float32') / 255.0
    # flatten for simple MLP; for conv nets you'd keep 28x28x1
    x_train = x_train.reshape((-1, 28*28))
    x_test = x_test.reshape((-1, 28*28))
    return x_train.astype(np.float32), x_test.astype(np.float32), y_train.astype(np.int64), y_test.astype(np.int64)


def load_mnist_for_torch(root='./data'):
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])
    train = datasets.MNIST(root=root, train=True, download=True, transform=transform)
    test = datasets.MNIST(root=root, train=False, download=True, transform=transform)
    return train, test

# -----------------------
# Torch model definition
# -----------------------
class TorchMLP(nn.Module):
    def __init__(self, n_features, n_classes=1, for_mnist=False):
        super().__init__()
        if for_mnist:
            # simple conv net for MNIST
            self.net = nn.Sequential(
                nn.Conv2d(1, 16, 3, padding=1),
                nn.ReLU(),
                nn.MaxPool2d(2),
                nn.Conv2d(16, 32, 3, padding=1),
                nn.ReLU(),
                nn.MaxPool2d(2),
                nn.Flatten(),
                nn.Linear(32 * 7 * 7, 128),
                nn.ReLU(),
                nn.Linear(128, 10)
            )
        else:
            self.net = nn.Sequential(
                nn.Linear(n_features, 64),
                nn.ReLU(),
                nn.Linear(64, 32),
                nn.ReLU(),
                nn.Linear(32, n_classes)
            )

    def forward(self, x):
        return self.net(x)

# -----------------------
# QThread trainers
# -----------------------
class TFTrainer(QThread):
    progress = pyqtSignal(int)
    log = pyqtSignal(str)
    finished_signal = pyqtSignal(dict)
    history_signal = pyqtSignal(object)

    def __init__(self, X_train, y_train, X_test, y_test, params, for_mnist=False):
        super().__init__()
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test
        self.params = params
        self.for_mnist = for_mnist

    def run(self):
        try:
            tf.keras.backend.clear_session()
            self.log.emit('TF: construction du modèle...')
            if self.for_mnist:
                # simple conv model
                model = tf.keras.Sequential([
                    tf.keras.layers.Reshape((28,28,1), input_shape=(28*28,)),
                    tf.keras.layers.Conv2D(16, 3, activation='relu', padding='same'),
                    tf.keras.layers.MaxPool2D(),
                    tf.keras.layers.Conv2D(32, 3, activation='relu', padding='same'),
                    tf.keras.layers.MaxPool2D(),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(128, activation='relu'),
                    tf.keras.layers.Dense(10, activation='softmax')
                ])
                loss = 'sparse_categorical_crossentropy'
                metrics = ['accuracy']
            else:
                n_features = self.X_train.shape[1]
                model = tf.keras.Sequential([
                    tf.keras.layers.Input(shape=(n_features,)),
                    tf.keras.layers.Dense(64, activation='relu'),
                    tf.keras.layers.Dense(32, activation='relu'),
                    tf.keras.layers.Dense(1, activation='sigmoid')
                ])
                loss = 'binary_crossentropy'
                metrics = ['accuracy']

            model.compile(optimizer=tf.keras.optimizers.Adam(self.params['lr']), loss=loss, metrics=metrics)

            class QtCallback(tf.keras.callbacks.Callback):
                def __init__(self, outer):
                    super().__init__()
                    self.outer = outer
                def on_epoch_end(self, epoch, logs=None):
                    percent = int((epoch + 1) / self.outer.params['epochs'] * 100)
                    msg = f"TF: Epoch {epoch+1}/{self.outer.params['epochs']} - loss={logs.get('loss'):.4f}"
                    if 'accuracy' in logs:
                        msg += f", acc={logs.get('accuracy'):.4f}"
                    self.outer.log.emit(msg)
                    self.outer.progress.emit(percent)

            self.log.emit('TF: démarrage training...')
            history = model.fit(self.X_train, self.y_train,
                                validation_data=(self.X_test, self.y_test),
                                epochs=self.params['epochs'],
                                batch_size=self.params['batch_size'],
                                verbose=0,
                                callbacks=[QtCallback(self)])

            eval_res = model.evaluate(self.X_test, self.y_test, verbose=0)
            res = {'framework': 'tensorflow', 'eval': eval_res}
            # save model object and history for UI
            res['model'] = model
            res['history'] = history.history
            self.log.emit('TF: training terminé.')
            self.finished_signal.emit(res)
            self.history_signal.emit(history.history)
        except Exception as e:
            tb = traceback.format_exc()
            self.log.emit('TF Error: ' + str(e))
            self.log.emit(tb)
            self.finished_signal.emit({'framework':'tensorflow','error':str(e)})


class TorchTrainer(QThread):
    progress = pyqtSignal(int)
    log = pyqtSignal(str)
    finished_signal = pyqtSignal(dict)
    history_signal = pyqtSignal(object)

    def __init__(self, train_ds, test_ds, params, for_mnist=False):
        super().__init__()
        self.train_ds = train_ds
        self.test_ds = test_ds
        self.params = params
        self.for_mnist = for_mnist

    def run(self):
        try:
            device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            self.log.emit(f'Torch: device {device}')
            if self.for_mnist:
                model = TorchMLP(None, for_mnist=True).to(device)
                criterion = nn.CrossEntropyLoss()
            else:
                n_features = self.train_ds.tensors[0].shape[1]
                model = TorchMLP(n_features, n_classes=1, for_mnist=False).to(device)
                criterion = nn.BCEWithLogitsLoss()

            optimizer = optim.Adam(model.parameters(), lr=self.params['lr'])
            train_loader = DataLoader(self.train_ds, batch_size=self.params['batch_size'], shuffle=True)
            test_loader = DataLoader(self.test_ds, batch_size=self.params['batch_size'])

            history = {'loss': [], 'acc': []}
            for epoch in range(self.params['epochs']):
                model.train()
                running = 0.0
                for xb, yb in train_loader:
                    xb = xb.to(device)
                    yb = yb.to(device)
                    optimizer.zero_grad()
                    preds = model(xb)
                    if self.for_mnist:
                        loss = criterion(preds, yb.long())
                    else:
                        loss = criterion(preds, yb.unsqueeze(1))
                    loss.backward()
                    optimizer.step()
                    running += loss.item() * xb.size(0)
                epoch_loss = running / len(train_loader.dataset)

                # évaluation
                model.eval()
                correct = 0
                total = 0
                with torch.no_grad():
                    for xb, yb in test_loader:
                        xb = xb.to(device)
                        yb = yb.to(device)
                        preds = model(xb)
                        if self.for_mnist:
                            predicted = preds.argmax(dim=1)
                            correct += (predicted == yb).sum().item()
                            total += yb.size(0)
                        else:
                            predicted = (torch.sigmoid(preds) >= 0.5).float()
                            correct += (predicted == yb.unsqueeze(1)).sum().item()
                            total += yb.size(0)
                acc = correct / total if total > 0 else 0
                history['loss'].append(epoch_loss)
                history['acc'].append(acc)
                percent = int((epoch + 1) / self.params['epochs'] * 100)
                self.log.emit(f'Torch: Epoch {epoch+1}/{self.params["epochs"]} - loss={epoch_loss:.4f}, acc={acc:.4f}')
                self.progress.emit(percent)
                time.sleep(0.01)

            self.log.emit('Torch: training terminé.')
            self.finished_signal.emit({'framework':'torch','model':model,'history':history})
            self.history_signal.emit(history)
        except Exception as e:
            tb = traceback.format_exc()
            self.log.emit('Torch Error: ' + str(e))
            self.log.emit(tb)
            self.finished_signal.emit({'framework':'torch','error':str(e)})

# -----------------------
# Main Window UI
# -----------------------
class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = fig.add_subplot(111)
        super().__init__(fig)
        self.setParent(parent)

    def plot(self, data: dict, title=''):
        self.ax.clear()
        # data may contain 'loss'/'acc' or keras history
        if 'loss' in data:
            self.ax.plot(data['loss'], label='loss')
        if 'val_loss' in data:
            self.ax.plot(data.get('val_loss'), '--', label='val_loss')
        if 'accuracy' in data:
            self.ax.plot(data.get('accuracy'), label='acc')
        if 'val_accuracy' in data:
            self.ax.plot(data.get('val_accuracy'), '--', label='val_acc')
        if 'acc' in data and isinstance(data['acc'], list):
            self.ax.plot(data['acc'], label='acc')
        self.ax.set_title(title)
        self.ax.legend()
        self.draw()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('AI Trainer — TF + Torch + PyQt5 (complet)')
        self.resize(1100, 700)
        self._build_ui()
        # placeholders
        self.tf_model = None
        self.torch_model = None
        self.tf_history = None
        self.torch_history = None
        # default data: synthetic
        self.dataset_type = 'synthetic'
        self.X_train, self.X_test, self.y_train, self.y_test = generate_synthetic()
        self.torch_train_ds = None
        self.torch_test_ds = None

    def _build_ui(self):
        main_layout = QHBoxLayout()

        left = QVBoxLayout()
        right = QVBoxLayout()

        # Data & params group
        data_group = QGroupBox('Dataset & Hyperparams')
        dg_layout = QGridLayout()

        self.dataset_combo = QComboBox()
        self.dataset_combo.addItems(['synthetic', 'mnist'])
        self.dataset_combo.currentTextChanged.connect(self.on_dataset_change)
        dg_layout.addWidget(QLabel('Dataset'), 0, 0)
        dg_layout.addWidget(self.dataset_combo, 0, 1)

        self.epochs_spin = QSpinBox(); self.epochs_spin.setRange(1, 200); self.epochs_spin.setValue(8)
        dg_layout.addWidget(QLabel('Epochs'), 1, 0); dg_layout.addWidget(self.epochs_spin, 1, 1)
        self.batch_spin = QSpinBox(); self.batch_spin.setRange(1, 1024); self.batch_spin.setValue(64)
        dg_layout.addWidget(QLabel('Batch size'), 2, 0); dg_layout.addWidget(self.batch_spin, 2, 1)
        self.lr_spin = QDoubleSpinBox(); self.lr_spin.setRange(1e-6, 1.0); self.lr_spin.setDecimals(6); self.lr_spin.setValue(1e-3)
        dg_layout.addWidget(QLabel('LR'), 3, 0); dg_layout.addWidget(self.lr_spin, 3, 1)

        data_group.setLayout(dg_layout)
        left.addWidget(data_group)

        # Buttons for TF
        tf_group = QGroupBox('TensorFlow')
        tf_layout = QVBoxLayout()
        btn_tf_train = QPushButton('Entraîner TF')
        btn_tf_save = QPushButton('Sauvegarder TF')
        btn_tf_load = QPushButton('Charger TF')
        tf_layout.addWidget(btn_tf_train); tf_layout.addWidget(btn_tf_save); tf_layout.addWidget(btn_tf_load)
        tf_group.setLayout(tf_layout)
        left.addWidget(tf_group)

        # Buttons for Torch
        torch_group = QGroupBox('PyTorch')
        torch_layout = QVBoxLayout()
        btn_torch_train = QPushButton('Entraîner Torch')
        btn_torch_save = QPushButton('Sauvegarder Torch')
        btn_torch_load = QPushButton('Charger Torch')
        torch_layout.addWidget(btn_torch_train); torch_layout.addWidget(btn_torch_save); torch_layout.addWidget(btn_torch_load)
        torch_group.setLayout(torch_layout)
        left.addWidget(torch_group)

        # Misc buttons
        misc_group = QGroupBox('Affichage / Prévisions')
        mg_layout = QVBoxLayout()
        btn_show_sample = QPushButton('Afficher un échantillon (MNIST si sélectionné)')
        btn_predict_sample = QPushButton('Prédire échantillon (TF/Torch)')
        mg_layout.addWidget(btn_show_sample); mg_layout.addWidget(btn_predict_sample)
        misc_group.setLayout(mg_layout)
        left.addWidget(misc_group)

        # Log and list of models
        self.log = QTextEdit(); self.log.setReadOnly(True)
        left.addWidget(QLabel('Logs'))
        left.addWidget(self.log)

        # Connect signals to methods
        btn_tf_train.clicked.connect(self.on_train_tf)
        btn_tf_save.clicked.connect(self.on_save_tf)
        btn_tf_load.clicked.connect(self.on_load_tf)
        btn_torch_train.clicked.connect(self.on_train_torch)
        btn_torch_save.clicked.connect(self.on_save_torch)
        btn_torch_load.clicked.connect(self.on_load_torch)
        btn_show_sample.clicked.connect(self.on_show_sample)
        btn_predict_sample.clicked.connect(self.on_predict_sample)

        # Right side: progress bars + plots + sample display
        self.pbar_tf = QProgressBar(); self.pbar_tf.setFormat('TF: %p%')
        self.pbar_torch = QProgressBar(); self.pbar_torch.setFormat('Torch: %p%')
        right.addWidget(self.pbar_tf); right.addWidget(self.pbar_torch)

        self.plot_canvas = PlotCanvas(self, width=6, height=4)
        right.addWidget(self.plot_canvas)

        # sample image list
        self.sample_list = QListWidget(); self.sample_list.setMaximumWidth(200)
        right.addWidget(QLabel('Exemples (MNIST)'))
        right.addWidget(self.sample_list)

        main_layout.addLayout(left, 3)
        main_layout.addLayout(right, 5)

        self.setLayout(main_layout)

    def append_log(self, text):
        ts = time.strftime('%H:%M:%S')
        self.log.append(f'[{ts}] {text}')
        self.log.verticalScrollBar().setValue(self.log.verticalScrollBar().maximum())

    def on_dataset_change(self, text):
        self.dataset_type = text
        self.append_log(f'Dataset changé: {text}')
        if text == 'synthetic':
            self.X_train, self.X_test, self.y_train, self.y_test = generate_synthetic()
            # prepare torch datasets for synthetic
            self.torch_train_ds = TensorDataset(torch.from_numpy(self.X_train), torch.from_numpy(self.y_train).float())
            self.torch_test_ds = TensorDataset(torch.from_numpy(self.X_test), torch.from_numpy(self.y_test).float())
            self.sample_list.clear()
        else:
            # MNIST
            self.append_log('Téléchargement MNIST (cela peut prendre un peu)...')
            xtr, xts, ytr, yts = load_mnist_for_tf()
            self.X_train, self.X_test, self.y_train, self.y_test = xtr, xts, ytr, yts
            train_ds, test_ds = load_mnist_for_torch()
            self.torch_train_ds = train_ds
            self.torch_test_ds = test_ds
            # fill sample list with a few indices
            self.sample_list.clear()
            for i in range(20):
                self.sample_list.addItem(f'Index {i} - label {self.torch_test_ds[i][1]}')

    def _collect_params(self):
        return {'epochs': int(self.epochs_spin.value()), 'batch_size': int(self.batch_spin.value()), 'lr': float(self.lr_spin.value())}

    # ---------------- TF actions ----------------
    def on_train_tf(self):
        params = self._collect_params()
        self.append_log('Lancement TF...')
        for_mnist = (self.dataset_type == 'mnist')
        self.tf_worker = TFTrainer(self.X_train, self.y_train, self.X_test, self.y_test, params, for_mnist=for_mnist)
        self.tf_worker.progress.connect(self.pbar_tf.setValue)
        self.tf_worker.log.connect(self.append_log)
        self.tf_worker.finished_signal.connect(self.on_tf_finished)
        self.tf_worker.history_signal.connect(self.on_tf_history)
        self.tf_worker.start()

    def on_tf_finished(self, res):
        if 'error' in res:
            self.append_log('TF erreur: ' + res['error'])
            return
        self.tf_model = res.get('model')
        self.tf_history = res.get('history')
        self.append_log('TF: modèle prêt. Tu peux sauvegarder le modèle.')

    def on_tf_history(self, history):
        self.append_log('TF: réception history pour plot')
        self.tf_history = history
        self.plot_canvas.plot(history, title='TF Training')

    def on_save_tf(self):
        if not self.tf_model:
            QMessageBox.warning(self, 'Avertissement', 'Aucun modèle TF chargé. Entraîne d\'abord.')
            return
        path = QFileDialog.getExistingDirectory(self, 'Choisir un dossier pour sauvegarder le modèle')
        if not path:
            return
        save_path = os.path.join(path, 'tf_model')
        try:
            self.tf_model.save(save_path)
            self.append_log(f'TF: modèle sauvegardé dans {save_path}')
        except Exception as e:
            self.append_log('TF Save Error: ' + str(e))

    def on_load_tf(self):
        path = QFileDialog.getExistingDirectory(self, 'Choisir le dossier contenant model TF (tf_model)')
        if not path:
            return
        try:
            model = tf.keras.models.load_model(path)
            self.tf_model = model
            self.append_log('TF: modèle chargé avec succès.')
        except Exception as e:
            self.append_log('TF Load Error: ' + str(e))

    # ---------------- Torch actions ----------------
    def on_train_torch(self):
        params = self._collect_params()
        self.append_log('Lancement Torch...')
        for_mnist = (self.dataset_type == 'mnist')
        # if mnist, train_ds/test_ds are torchvision datasets; else TensorDataset
        if for_mnist:
            train_ds = self.torch_train_ds
            test_ds = self.torch_test_ds
        else:
            train_ds = self.torch_train_ds
            test_ds = self.torch_test_ds
        self.torch_worker = TorchTrainer(train_ds, test_ds, params, for_mnist=for_mnist)
        self.torch_worker.progress.connect(self.pbar_torch.setValue)
        self.torch_worker.log.connect(self.append_log)
        self.torch_worker.finished_signal.connect(self.on_torch_finished)
        self.torch_worker.history_signal.connect(self.on_torch_history)
        self.torch_worker.start()

    def on_torch_finished(self, res):
        if 'error' in res:
            self.append_log('Torch erreur: ' + res['error'])
            return
        self.torch_model = res.get('model')
        self.torch_history = res.get('history')
        self.append_log('Torch: modèle prêt. Tu peux sauvegarder le modèle.')

    def on_torch_history(self, history):
        self.append_log('Torch: réception history pour plot')
        self.torch_history = history
        self.plot_canvas.plot(history, title='Torch Training')

    def on_save_torch(self):
        if not self.torch_model:
            QMessageBox.warning(self, 'Avertissement', 'Aucun modèle Torch chargé. Entraîne d\'abord.')
            return
        path, _ = QFileDialog.getSaveFileName(self, 'Sauvegarder modèle Torch', filter='PyTorch model (*.pt)')
        if not path:
            return
        try:
            torch.save(self.torch_model.state_dict(), path)
            self.append_log(f'Torch: modèle sauvegardé dans {path}')
        except Exception as e:
            self.append_log('Torch Save Error: ' + str(e))

    def on_load_torch(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Charger modèle Torch', filter='PyTorch model (*.pt)')
        if not path:
            return
        try:
            # attempt to reconstruct architecture based on dataset
            if self.dataset_type == 'mnist':
                model = TorchMLP(None, for_mnist=True)
            else:
                n_features = self.X_train.shape[1]
                model = TorchMLP(n_features, n_classes=1, for_mnist=False)
            model.load_state_dict(torch.load(path, map_location='cpu'))
            model.eval()
            self.torch_model = model
            self.append_log('Torch: modèle chargé avec succès.')
        except Exception as e:
            self.append_log('Torch Load Error: ' + str(e))

    # ---------------- Samples & predictions ----------------
    def on_show_sample(self):
        if self.dataset_type != 'mnist':
            QMessageBox.information(self, 'Info', 'Affichage d\'échantillons disponible uniquement pour MNIST.')
            return
        # show a simple grid of first 9 test images by opening a matplotlib window on canvas
        import matplotlib.pyplot as plt
        imgs = self.X_test[:9].reshape((-1,28,28))
        labels = self.y_test[:9]
        fig, axes = plt.subplots(3,3, figsize=(6,6))
        for i, ax in enumerate(axes.flat):
            ax.imshow(imgs[i], cmap='gray')
            ax.set_title(str(labels[i]))
            ax.axis('off')
        plt.show()

    def on_predict_sample(self):
        if self.dataset_type != 'mnist':
            QMessageBox.information(self, 'Info', 'Prédiction d\'échantillon prévue uniquement pour MNIST.')
            return
        idx = 0
        if self.sample_list.currentRow() >= 0:
            idx = self.sample_list.currentRow()
        x = self.X_test[idx:idx+1]
        # TF predict
        if self.tf_model:
            try:
                probs = self.tf_model.predict(x)
                if probs.shape[-1] == 10:
                    pred = int(np.argmax(probs, axis=1)[0])
                else:
                    pred = int((probs >= 0.5).astype(int)[0][0])
                self.append_log(f'TF prediction index {idx} -> {pred}')
            except Exception as e:
                self.append_log('TF Predict Error: ' + str(e))
        else:
            self.append_log('TF: pas de modèle chargé.')
        # Torch predict (need to convert)
        if self.torch_model:
            try:
                model = self.torch_model
                model.eval()
                if self.dataset_type == 'mnist':
                    import torch.nn.functional as F
                    x_t = torch.from_numpy(x.reshape((-1,28,28))).unsqueeze(1).float()
                    with torch.no_grad():
                        out = model(x_t)
                        pred = int(out.argmax(dim=1)[0].item())
                    self.append_log(f'Torch prediction index {idx} -> {pred}')
                else:
                    x_t = torch.from_numpy(x).float()
                    with torch.no_grad():
                        out = torch.sigmoid(model(x_t))
                        pred = int((out >= 0.5).cpu().numpy()[0][0])
                    self.append_log(f'Torch prediction index {idx} -> {pred}')
            except Exception as e:
                self.append_log('Torch Predict Error: ' + str(e))
        else:
            self.append_log('Torch: pas de modèle chargé.')

# -----------------------
# Main
# -----------------------

def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
