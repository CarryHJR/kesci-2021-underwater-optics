_base_ = [
    '../_base_/models/universenet50.py',
    '../_base_/datasets/nightowls_mstrain_640_1280.py',
    '../_base_/schedules/schedule_7e.py', '../_base_/default_runtime.py'
]
model = dict(bbox_head=dict(num_classes=3))

img_norm_cfg = dict(
    mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375], to_rgb=True)
test_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(
        type='MultiScaleFlipAug',
        img_scale=[(1280, 800), (1536, 960)],
        flip=True,
        transforms=[
            dict(type='Resize', keep_ratio=True),
            dict(type='RandomFlip'),
            dict(type='Normalize', **img_norm_cfg),
            dict(type='Pad', size_divisor=32),
            dict(type='ImageToTensor', keys=['img']),
            dict(type='Collect', keys=['img']),
        ])
]

data = dict(samples_per_gpu=4, test=dict(pipeline=test_pipeline))

optimizer = dict(type='SGD', lr=0.001, momentum=0.9, weight_decay=0.0001)

test_cfg = dict(
    nms_pre=1000,
    min_bbox_size=0,
    score_thr=0.02,
    nms=dict(type='nms', iou_threshold=0.6),
    max_per_img=1000)

fp16 = dict(loss_scale=512.)

load_from = '../data/checkpoints/universenet50_fp16_8x2_lr0001_mstrain_640_1280_7e_waymo_open_20200526_080330/epoch_7_for_nightowls.pth'  # noqa