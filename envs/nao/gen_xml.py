import sys
import os
from dm_control import mjcf
import random
import string

JVRC_DESCRIPTION_PATH="models\\nao_description-master\\urdf\\nao_fin.xml"

def builder(export_path):

    print("Modifying XML model...")
    mjcf_model = mjcf.from_path(JVRC_DESCRIPTION_PATH)
    
     # remove all collisions
    mjcf_model.contact.remove()

    head_joints = ['HeadYaw','HeadPitch']
    hand_joints = ['RFinger23','RFinger13','RFinger12','LFinger21','LFinger13','LFinger11',
                   'RFinger22','LFinger22','RFinger21','LFinger12','RFinger11','LFinger23','LThumb1','RThumb1','RThumb2','LThumb2']
    arm_joints = ['LShoulderPitch','LShoulderRoll','LElbowYaw','LElbowRoll','LWristYaw','LHand','RShoulderPitch','RShoulderRoll','RElbowYaw','RElbowRoll','RWristYaw','RHand']
    leg_joints = ['LHipYawPitch','LHipRoll','LHipPitch','LKneePitch','LAnklePitch','LAnkleRoll','RHipYawPitch','RHipRoll','RHipPitch','RKneePitch','RAnklePitch','RAnkleRoll']

    # remove actuators except for leg joints
    for mot in mjcf_model.actuator.motor:
        if mot.joint.name not in leg_joints:
            mot.remove()

    # remove unused joints
    for joint in  head_joints + hand_joints + arm_joints:
        mjcf_model.find('joint', joint).remove()

    # remove existing equality
    mjcf_model.equality.remove()

  
  # add equality for arm joints
    arm_joints = ['RShoulderPitch', 'RShoulderRoll', 'RElbowYaw',
                  'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw']
    mjcf_model.equality.add('joint', joint1=arm_joints[0], polycoef='-0.052 0 0 0 0')
    mjcf_model.equality.add('joint', joint1=arm_joints[1], polycoef='-0.169 0 0 0 0')
    mjcf_model.equality.add('joint', joint1=arm_joints[2], polycoef='-0.523 0 0 0 0')
    mjcf_model.equality.add('joint', joint1=arm_joints[3], polycoef='-0.052 0 0 0 0')
    mjcf_model.equality.add('joint', joint1=arm_joints[4], polycoef='0.169 0 0 0 0')
    mjcf_model.equality.add('joint', joint1=arm_joints[5], polycoef='-0.523 0 0 0 0')

    # collision geoms
    collision_geoms = [
        'RHipRoll', 'RHipYawPitch', 'RKneePitch',
        'LHipRoll', 'LHipYawPitch', 'LKneePitch',
    ]

    # remove unused collision geoms
    for body in mjcf_model.worldbody.find_all('body'):
        for idx, geom in enumerate(body.geom):
            geom.name = body.name + '-geom-' + repr(idx)
            if (geom.dclass.dclass=="collision"):
                if body.name not in collision_geoms:
                    geom.remove()

    # manually create collision geom for feet
    mjcf_model.worldbody.find('body', 'RAnklePitch').add('geom', dclass='collision', size='0.1 0.05 0.01', pos='0.029 0 -0.09778', type='box')
    mjcf_model.worldbody.find('body', 'LAnklePitch').add('geom', dclass='collision', size='0.1 0.05 0.01', pos='0.029 0 -0.09778', type='box')

    # ignore collision
    mjcf_model.contact.add('exclude', body1='RKneePitch', body2='RAnklePitch')
    mjcf_model.contact.add('exclude', body1='LKneePitch', body2='LAnklePitch')

    # remove unused meshes
    meshes = [g.mesh.name for g in mjcf_model.find_all('geom') if g.type=='mesh' or g.type==None]
    for mesh in mjcf_model.find_all('mesh'):
        if mesh.name not in meshes:
            mesh.remove()

 

    # add box geoms
    for idx in range(20):
        mjcf_model.worldbody.add('geom',
                                 name='box' + repr(idx+1).zfill(2),
                                 pos='0 0 -0.2',
                                 dclass='collision',
                                 group='0',
                                 size='1 1 0.1',
                                 type='box',
                                 material='')

    # export model
    mjcf.export_with_assets(mjcf_model, out_dir=os.path.dirname(export_path), out_file_name=export_path, precision=5)
    print("Exporting XML model to ", export_path)
    return

if __name__=='__main__':
    builder(sys.argv[1])
