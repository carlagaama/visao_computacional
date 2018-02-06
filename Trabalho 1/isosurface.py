# File:        isosurface.py
# Description: Iso-surface extraction from a volume
#              Run this example from a command prompt by typing:
#              "python isosurface.py"

import vtk

# image reader
filename = "hydrogen.vtk"
reader = vtk.vtkStructuredPointsReader()
reader.SetFileName( filename )
# must call Update() before we fetch the dimensions
reader.Update()
# just for illustration:
# get the extent of the data and print it
W,H,D = reader.GetOutput().GetDimensions()
# string formatting is similar to the sprintf style in C
print "Reading '%s', width=%i, height=%i, depth=%i" %(filename, W, H, D)

# create an outline of the dataset
outline = vtk.vtkOutlineFilter()
outline.SetInputConnection( reader.GetOutputPort() )
outlineMapper = vtk.vtkPolyDataMapper()
outlineMapper.SetInputConnection( outline.GetOutputPort() )
outlineActor = vtk.vtkActor()
outlineActor.SetMapper( outlineMapper )

# the actors property defines color, shading, line width,...
outlineActor.GetProperty().SetColor(0.0,0.0,1.0)
outlineActor.GetProperty().SetLineWidth(2.0)

#
# add your code here...
#
# paleta de cores RGB
paleta = vtk.vtkColorTransferFunction()
paleta.AddRGBPoint(0, 1, 0, 0)
paleta.AddRGBPoint(0.5, 1, 1, 0)
paleta.AddRGBPoint(1, 0, 1, 0)
# paleta = vtk.vtkLookupTable()
paleta.Build()

# metodo para setar corretamene a escala de cores scala bar
output = reader.GetOutput()
mapper = vtk.vtkDataSetMapper()
if vtk.VTK_MAJOR_VERSION <= 5:
    mapper.SetInput(output)
else:
    mapper.SetInputData(output)
mapper.SetLookupTable(paleta)

isoSurface = vtk.vtkContourFilter()
isoSurface.SetInputConnection(reader.GetOutputPort())
# valor inicial
val = 0.5
isoSurface.SetValue(0, val)
#
surfaceMapper = vtk.vtkPolyDataMapper()
surfaceMapper.SetLookupTable(paleta)
surfaceMapper.SetInputConnection(isoSurface.GetOutputPort())
surfaceActor = vtk.vtkActor()
surfaceActor.SetMapper(surfaceMapper)

# probabilidade
textActor = vtk.vtkTextActor()
# propriedades do texto da probabilidade
prop_texto = vtk.vtkTextProperty()
prop_texto.SetFontSize(40)
textActor.SetTextProperty(prop_texto)
pos_texto = textActor.GetPositionCoordinate()
pos_texto.SetCoordinateSystemToNormalizedViewport()
pos_texto.SetValue(0.01,0.9)
prop_texto.SetColor(paleta.GetColor(val))
textActor.SetInput("%.2f" %(val))

# renderer and render window
ren = vtk.vtkRenderer()
ren.SetBackground(.8, .8, .8)
renWin = vtk.vtkRenderWindow()
renWin.SetSize( 400, 400 )
renWin.AddRenderer( ren )

# render window interactor
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow( renWin )

# add the actors
ren.AddActor( outlineActor )
ren.AddActor(surfaceActor)
ren.AddActor(textActor)

renWin.Render()

# create window to image filter to get the window to an image
w2if = vtk.vtkWindowToImageFilter()
w2if.SetInput(renWin)

# create png writer
wr = vtk.vtkPNGWriter()
wr.SetInputConnection(w2if.GetOutputPort())

# gerando o scalarBar https://www.vtk.org/Wiki/VTK/Examples/Python/Widgets/ScalarBarWidget
scalarBar = vtk.vtkScalarBarActor()
scalarBar.SetOrientationToHorizontal()
scalarBar.SetLookupTable(surfaceMapper.GetLookupTable())
scalarBar.GetLabelTextProperty().SetColor(0,0,0)
scalarBar.GetTitleTextProperty().SetColor(0,0,0)
scalarBar.SetTitle("probabilidade")
scalarBar_widget = vtk.vtkScalarBarWidget()
scalarBar_widget.SetInteractor(iren)
scalarBar_widget.SetScalarBarActor(scalarBar)
scalarBar_widget.On()
scalarBar_widget.RepositionableOff()

# Python function for the keyboard interface
# count is a screenshot counter
count = 0
def Keypress(obj, event):
    global count, iv, val, renWin, w2if
    key = obj.GetKeySym()
    if key == "s":
        renWin.Render()
        w2if.Modified()
        fnm = "screenshot%02d.png" %(count)
        wr.SetFileName(fnm)
        wr.Write()
        print "Saved '%s'" %(fnm)
        count = count + 1
    elif key == "KP_Add":
        val += 0.01;
        isoSurface.SetValue(0, val)
        textActor.SetInput("%.2f" %(val))
        prop_texto.SetColor(paleta.GetColor(val))
        renWin.Render()
        w2if.Modified()

    elif key == "KP_Subtract":
        val -= 0.01;
        isoSurface.SetValue(0, val)
        textActor.SetInput("%.2f" %(val))
        prop_texto.SetColor(paleta.GetColor(val))
        renWin.Render()
        w2if.Modified()

# add keyboard interface, initialize, and start the interactor
iren.AddObserver("KeyPressEvent", Keypress)
renWin.Render()

iren.Initialize()
iren.Start()
