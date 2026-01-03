from PyQt5 import QtWidgets, uic
import sys
import vtk
import numpy as np
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("vtk_layout.ui", self)

        # =========================
        # VTK inside Qt
        # =========================
        self.vtk_widget = QVTKRenderWindowInteractor(self.vtk_frame)

        layout = self.vtk_frame.layout()
        if layout is None:
            layout = QtWidgets.QVBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            self.vtk_frame.setLayout(layout)
        layout.addWidget(self.vtk_widget)

        self.renderer = vtk.vtkRenderer()
        self.vtk_widget.GetRenderWindow().AddRenderer(self.renderer)

        # =========================
        # TEST VOLUME (finto)
        # =========================
        vol = np.random.rand(128, 128, 64).astype(np.float32) * 255

        vtk_img = vtk.vtkImageData()
        vtk_img.SetDimensions(vol.shape)
        vtk_img.AllocateScalars(vtk.VTK_FLOAT, 1)

        for z in range(vol.shape[2]):
            for y in range(vol.shape[1]):
                for x in range(vol.shape[0]):
                    vtk_img.SetScalarComponentFromFloat(x, y, z, 0, vol[x, y, z])

        # =========================
        # Image slice actor
        # =========================

        self.slice_actor = vtk.vtkImageActor()
        self.slice_actor.GetMapper().SetInputData(vtk_img)

        self.slice_actor.GetProperty().SetColorWindow(255)
        self.slice_actor.GetProperty().SetColorLevel(127)

        z_mid = vol.shape[2] // 2
        self.slice_actor.SetDisplayExtent(
            0, vol.shape[0] - 1,
            0, vol.shape[1] - 1,
            z_mid, z_mid
        )

        self.renderer.AddActor(self.slice_actor)
        self.renderer.ResetCamera()

        self.vtk_widget.GetRenderWindow().Render()

    

        # IMPORTANT: no Start(), no Initialize()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
