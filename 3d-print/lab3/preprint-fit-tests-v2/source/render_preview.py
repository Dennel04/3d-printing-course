from pathlib import Path
import trimesh,numpy as np,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.patches import FancyBboxPatch
root=Path(__file__).resolve().parents[1]
scene=trimesh.load_scene(root/'3MF/LAB3_FIT_TESTS_ONE_PLATE.3mf')
colors=['#7961b7','#3f83aa','#cca568','#60a5a0','#dc956c']
labels=['1 · UV shroud','2 · Syringe clip','3 · Purge cup','4 · Nozzle park','5 · O-ring coupon']
fig=plt.figure(figsize=(14,7.3),dpi=150,facecolor='#fbfbfd')
ax=fig.add_subplot(121,projection='3d',computed_zorder=False)
ax2=fig.add_subplot(122)
for node in scene.graph.nodes_geometry:
    transform,geom_key=scene.graph[node]
    i=int(geom_key[:2])-1
    mesh=scene.geometry[geom_key].copy();mesh.apply_transform(transform)
    tri=mesh.vertices[mesh.faces]
    normals=mesh.face_normals
    light=np.array([0.4,-0.35,1.0]);light/=np.linalg.norm(light)
    shade=0.65+0.35*np.maximum(np.einsum('ij,j->i',normals,light),0)
    rgb=np.array(to_rgb(colors[i]));rgba=np.column_stack([np.clip(shade[:,None]*rgb,0,1),np.ones(len(shade))])
    poly=Poly3DCollection(tri,facecolors=rgba,edgecolors='none',zsort='average')
    ax.add_collection3d(poly)
    # Bounding rectangle indicates occupied footprint, not actual exact projected outline
    b=mesh.bounds
    box=FancyBboxPatch((b[0,0],b[0,1]), b[1,0]-b[0,0], b[1,1]-b[0,1],boxstyle='round,pad=0,rounding_size=2',facecolor=colors[i],edgecolor='#222633',alpha=.75,lw=1.2)
    ax2.add_patch(box)
    center=(b[0]+b[1])/2
    ax2.text(center[0],center[1],str(i+1),fontsize=17,fontweight='bold',color='#12121a',ha='center',va='center')
ax.set_xlim(0,165);ax.set_ylim(0,138);ax.set_zlim(0,60)
ax.set_box_aspect((165,138,60),zoom=.86)
ax.view_init(elev=30,azim=-65)
ax.set_xlabel('X (mm)',labelpad=7);ax.set_ylabel('Y (mm)',labelpad=7);ax.set_zlabel('Z (mm)',labelpad=5)
ax.set_title('Actual five solid meshes · isometric',fontsize=13,fontweight='bold',pad=16)
ax.xaxis.set_pane_color((0.98,0.98,1,1));ax.yaxis.set_pane_color((0.98,0.98,1,1));ax.zaxis.set_pane_color((0.98,0.98,1,1))
ax2.set_xlim(0,166);ax2.set_ylim(0,138);ax2.set_aspect('equal',adjustable='box');ax2.set_xlabel('X (mm)');ax2.set_ylabel('Y (mm)');ax2.set_title('Plate layout · bounding footprints',fontsize=13,fontweight='bold',pad=16)
ax2.grid(True,alpha=.16)
legend='     '.join(labels[:3])+'\n'+'     '.join(labels[3:])
fig.text(.5,.065,legend,ha='center',va='center',fontsize=10,color='#373744')
fig.suptitle('Lab 3  |  Print-fit prototypes, rev 2  |  CORE One',fontsize=16,fontweight='bold',y=.98)
fig.text(.5,.014,'CAD fit candidates only. Not a validated UV shield, pressure seal, or MG400 tool.',ha='center',fontsize=9,color='#ac3842')
fig.subplots_adjust(left=.03,right=.97,top=.84,bottom=.13,wspace=.1)
fig.savefig(root/'preview_plate.png',dpi=150,facecolor=fig.get_facecolor())
print(root/'preview_plate.png')
