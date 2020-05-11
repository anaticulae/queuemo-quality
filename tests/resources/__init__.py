# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import utila

import train

RESOURCES = os.path.join(train.ROOT, 'tests/resources')
assert os.path.exists(RESOURCES), RESOURCES

GENERATED = os.path.join(RESOURCES, 'generated')

MASTER72 = os.path.join(RESOURCES, 'master/page_72_noimages_toc.pdf')

FILES = utila.file_list(RESOURCES, include='pdf')
