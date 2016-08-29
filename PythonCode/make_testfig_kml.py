
"""
Code to test making a plot and turning it into a kml file.
Not working properly.
"""

from pylab import *

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

print "Created %s " % png_file


# make kml file:


text = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:atom="http://www.w3.org/2005/Atom"
xmlns="http://www.opengis.net/kml/2.2">
  <Document>
      <GroundOverlay>
        <name>%s.png</name>
        <Icon>
          <href>%s.png</href>
        </Icon>
        <LatLonBox>
          <north>%9.6f</north>
          <south>%9.6f</south>
          <east>%9.6f</east>
          <west>%9.6f</west>
        </LatLonBox>
      </GroundOverlay>
   </Document>
</kml>
""" % (fname,fname,y2,y1,x2,x1)

kml_file = open('%s.kml' % fname, 'w')
kml_file.write(text)
kml_file.close()
print "Created %s.kml" % fname
