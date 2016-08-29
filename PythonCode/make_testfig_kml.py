
"""
Code to test making a plot and turning it into a kml file.
Not working properly.
"""

from pylab import *
from lxml import etree
from pykml.factory import KML_ElementMaker as KML

# load sample data -- download etopo1 DEM if not already here:

from clawpack.geoclaw import etopotools
from clawpack.geoclaw import topotools

xlimits = (-126,-122)
ylimits = (46,49)
resolution = 1./60.   # in degrees

etopotools.etopo1_download(xlimits,ylimits, dx=resolution, \
        output_dir='../DataFiles', verbose=True)

topo = topotools.Topography()
topo.read('../DataFiles/etopo1_-126_-122_46_49_1min.asc', topo_type=3)

X = topo.X
Y = topo.Y
B = topo.Z   # topo elevation, negative is below sea level

x1 = X.min()
x2 = X.max()
y1 = Y.min()
y2 = Y.max()


# make sample plot:
# Color red where elevation between 0 and 100, yellow between 100 and 200:
fig = plt.figure(10)
contourf(X,Y,B,[0, 100, 200],colors=['r','y'],alpha=0.5)

#fig.patch.set_alpha(0)
a = fig.gca()
a.set_position([0.,0.,1.0,1.0])
a.set_frame_on(False)

# These have to be turned off explicitly so the plot doesn't have any
# padding.
a.set_xticks([])
a.set_yticks([])

# Figure out optimal settings (for best results when using
# transparency)
#kml_figsize = [30., 30.]
#rcl = 2
#kml_dpi = rcl*2*6   # Resolve course and fine grid

kml_figsize = None  # This should match aspect ratio of domain
kml_dpi = None

plt.axis('off')
if kml_figsize is not None:
    fig.set_size_inches(kml_figsize[0],kml_figsize[1])

fname = 'testfig'
png_file = fname + '.png'

plt.savefig(fname, transparent=True, bbox_inches='tight', \
            pad_inches=0,dpi=kml_dpi)

print "Created ",fname


# make kml file:

print "Creating %s.kml" % fname

kml_doc = KML.kml(KML.Document())
kml_doc.Document.append(KML.Style(
KML.ListStyle(
    KML.listItemType("radioFolder")),id="folderStyle"))  # "radioFolder" <--> "check"

kml_doc.Document.append(KML.Folder(
    KML.name("Grids"),
    KML.open(1)))


is_vis = 1

print "     Creating KML entry for %s" % png_file
go = KML.GroundOverlay(KML.name(f),
                       KML.visibility(is_vis),   # Only show first plot
                       KML.Icon(
                           KML.href(png_file)),
                       KML.LatLonBox(
                           KML.north(y1),
                           KML.south(y2),
                           KML.east(x2),
                           KML.west(x1)))
is_vis = 0

kml_doc.Document.Folder.append(go)

# Add style (check box or radio button)
kml_doc.Document.Folder.append(KML.styleUrl("#folderStyle"))


# --------------------------------------------
# Create the file <fname>.kml
# --------------------------------------------
docfile = open("%s.kml" % fname,'w')
docfile.write('<?xml version="1.0" encoding="UTF-8"?>\n')

kml_text = etree.tostring(etree.ElementTree(kml_doc),pretty_print=True)
docfile.write(kml_text)

docfile.close()

