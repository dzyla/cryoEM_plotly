import mrcfile
import numpy as np
import plotly
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
from skimage import measure


def open_mrcs_file(file_path):
    with mrcfile.open(file_path) as mrc_stack:
        return mrc_stack.data

#open the MRC or map file
file_path = 'EMD-6240.map'

data = np.array(open_mrcs_file(file_path))


#plot histogram of the intesities to see the data range
plt.hist(data.flatten(), bins=1000, log=True)
plt.show()

#based on the histogram choose the level which will be showed
#choose the value with is rather in the right
lvl = float(input('level: '))

#find the vertises and faces
verts, faces, normals, values = measure.marching_cubes_lewiner(data, level=lvl)

#Set the color of the surface based on the faces order. Here you can provide your own colouring
color = np.zeros(len(faces))
color[0] = 1  # because there has to be a colour range, 1st element is 1
color = list(color) #change numpy array to list

#create a plotly trisurf figure
fig = ff.create_trisurf(x=verts[:, 2],
                        y=verts[:, 1],
                        z=verts[:, 0],
                        plot_edges=False,
                        color_func=color,
                        simplices=faces,
                        showbackground=False,
                        show_colorbar=False
                        )

#remove axes
fig['layout'].update(scene = dict(xaxis = dict(visible=False),yaxis = dict(visible=False),zaxis = dict(visible=False)))

#plot the figure and show it in the browser
plotly.offline.plot(fig)
