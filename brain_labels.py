'''
2020-02-14 JS
All regions I've been able to find in PS tasks, either in the stim. electrode (see below)
or in the other electrodes (see get_elec_regions). These can be found in a manner like
the "unique electrode region labels" cell in dataQuality.ipynb
Can import like so: >>>from brain_labels import MTL_labels, LTC_labels, PFC_labels, OTHER_labels, ALL_labels

2020-08-17 JS updated with new labels now that I'm loading localization.json pairs in addition to usual pairs in FR1.
see SWRgetRegionNames for details on getting the region names and the order or operations for differnt atlases
in SWRmodule.
2020-09-04 JS checked this for catFR too and regions are the same
'''

MTL_stein = ['left ca1','left ca2','left ca3','left dg','left sub','left prc','left ec','left phc','left mtl wm',
             'right ca1','right ca2','right ca3','right dg','right sub','right prc','right ec','right phc','right mtl wm',
             'left amy','right amy'] # including amygdala in MTL
LTC_stein = ['left middle temporal gyrus','left stg','left mtg','left itg','left inferior temporal gyrus','left superior temporal gyrus', # never saw last 2 but why not?
             'right middle temporal gyrus','right stg','right mtg','right itg','right inferior temporal gyrus','right superior temporal gyrus'] #same
PFC_stein = ['left caudal middle frontal cortex','left dlpfc','left precentral gyrus','right precentral gyrus',
             'right caudal middle frontal cortex','right dlpfc','right superior frontal gyrus']
cingulate_stein = ['left acg','left mcg','left pcg','right acg','right pcg']
parietal_stein = ['left supramarginal gyrus','right supramarginal gyrus']
other_TL_stein = ['left fusiform gyrus wm'] # actually from Das. ba36 is part of fusiform
other_stein = ['left precentral gyrus','none','right insula','right precentral gyrus','nan','misc']

# Using Desikan Neuroimage (2016), the ind localizations come from automated segmentation
# I'm also adding in dk and wb to these, since for some reason those are used for some electrode regions
# -dk comes from the same DesikanKilliany(2006) paper
# -wb (whole-brain) appears to come from FreeSurfer labels here: 
# https://www.slicer.org/wiki/Documentation/4.1/SlicerApplication/LookupTables/Freesurfer_labels
# although Sandy Das pointed to http://www.neuromorphometrics.com/2012_MICCAI_Challenge_Data.html
# 2020-08-17 updated these with new values from loading wb and MTL fields in localization.json pairs
MTL_ind = ['parahippocampal','entorhinal','temporalpole',   
           ' left amygdala',' left ent entorhinal area',' left hippocampus',' left phg parahippocampal gyrus',' left tmp temporal pole', # whole-brain names
           ' right amygdala',' right ent entorhinal area',' right hippocampus',' right phg parahippocampal gyrus',' right tmp temporal pole',
           'left amygdala','left ent entorhinal area','left hippocampus','left phg parahippocampal gyrus','left tmp temporal pole',
           'right amygdala','right ent entorhinal area','right hippocampus','right phg parahippocampal gyrus','right tmp temporal pole',
           '"ba35"','"ba36"','"ca1"', '"dg"', '"erc"', '"phc"', '"sub"',
           'ba35', 'ba36','ca1','dg','erc','phc','sub']
LTC_ind = ['bankssts','middletemporal','inferiortemporal','superiortemporal', # first 4 defined by Ezzyat NatComm 2018...unsure about bankssts tho
           'left itg inferior temporal gyrus','left mtg middle temporal gyrus','left stg superior temporal gyrus',
           ' left itg inferior temporal gyrus',' left mtg middle temporal gyrus',' left stg superior temporal gyrus', 
           'right itg inferior temporal gyrus','right mtg middle temporal gyrus','right stg superior temporal gyrus', 
           ' right itg inferior temporal gyrus',' right mtg middle temporal gyrus',' right stg superior temporal gyrus']
           # leaving out 'left/right ttg transverse temporal gyrus' and 'transversetemporal'
           
# havne't below yet with new values from localization.json (the wb ones)
PFC_ind = ['caudalmiddlefrontal','frontalpole','lateralorbitofrontal','medialorbitofrontal','parsopercularis',
          'parsorbitalis','parstriangularis','rostralmiddlefrontal','superiorfrontal']
cingulate_ind = ['caudalanteriorcingulate','isthmuscingulate','posteriorcingulate','rostralanteriorcingulate']
parietal_ind = ['inferiorparietal','postcentral','precuneus','superiorparietal','supramarginal']
occipital_ind = ['cuneus','lateraloccipital','lingual','pericalcarine']
other_TL_ind = ['fusiform','transversetemporal'] # temporal lobe but not MTL
other_ind = ['insula','none','precentral','paracentral','right inf lat vent','left inf lat vent', # not sure where to put these
            'left cerebral white matter','right cerebral white matter', # these wb labels can be anywhere in hemisphere so just put in other
             'nan','left lateral ventricle','right lateral ventricle']

MTL_labels = MTL_stein+MTL_ind
LTC_labels = LTC_stein+LTC_ind
PFC_labels = PFC_stein+PFC_ind
OTHER_labels = cingulate_stein+parietal_stein+other_TL_stein+other_stein+ \
                cingulate_ind+occipital_ind+other_TL_ind+other_ind
ALL_labels = MTL_labels+LTC_labels+PFC_labels+OTHER_labels


# These are my DLPFC (~middle frontal gyrus) labels:
DLPFC_labels = ['rostralmiddlefrontal','caudalmiddlefrontal', 'Left DLPFC','Right DLPFC', 
        'Left MFG middle frontal gyrus','Right MFG middle frontal gyrus', 
        ' Left MFG middle frontal gyrus', 'Right MFG middle frontal gyrus',
        'Right Caudal Middle Frontal Cortex','Left Caudal Middle Frontal Cortex',
        'Brodmann area 46','Brodmann area 9']

DLPFC_labels=[word.lower() for word in DLPFC_labels]


'''
# This is the original, which only has labels for those places STIMULATED across PS tasks.
# The above has regions for the other (record-only) electrodes as well. I dunno why you'd want to use
# this smaller set below, but keeping it for posterity
# stim location labels
# these are all the regions that were stimulated in PS and locationSearch tasks
MTL_stein = ['left ca1','left ca2','left ca3','left dg','left sub','left prc','left ec','left phc',
             'right ca1','right ca2','right ca3','right dg','right sub','right prc','right ec',
             'right phc','left mtl wm','right mtl wm','left amy','right amy'] # including amygdala in MTL
LTC_stein = ['left middle temporal gyrus','right middle temporal gyrus','right stg']
PFC_stein = ['left caudal middle frontal cortex','left dlpfc','left precentral gyrus','right precentral gyrus',
             'right caudal middle frontal cortex','right dlpfc','right superior frontal gyrus']
cingulate_stein = ['left acg','left mcg','left pcg','right acg','right pcg']
parietal_stein = ['left supramarginal gyrus','right supramarginal gyrus']
other_TL_stein = ['ba36','left fusiform gyrus wm'] # actually from Das. ba36 is part of fusiform
other_stein = ['left precentral gyrus','none','right insula','right precentral gyrus']
# Using Desikan Neuroimage (2016), the ind localizations come from automated segmentation
MTL_ind = ['parahippocampal','entorhinal','temporalpole']
LTC_ind = ['bankssts','middletemporal','inferiortemporal','superiortemporal'] # as defined by Ezzyat NatComm 2018...unsure about bankssts tho
PFC_ind = ['caudalmiddlefrontal','frontalpole','lateralorbitofrontal','medialorbitofrontal','parsopercularis',
          'parsorbitalis','parstriangularis','rostralmiddlefrontal','superiorfrontal']
cingulate_ind = ['caudalanteriorcingulate','isthmuscingulate','posteriorcingulate','rostralanteriorcingulate']
parietal_ind = ['inferiorparietal','postcentral','precuneus','superiorparietal','supramarginal']
occipital_ind = ['cuneus','lateraloccipital','lingual','pericalcarine']
other_TL_ind = ['fusiform','transversetemporal'] # temporal lobe but not MTL
other_ind = ['insula','none','precentral','paracentral'] # not sure where to put these
'''

'''
This is the complete list of regions I found in the catFR dataset:
array(['Left DLPFC', 'medialorbitofrontal', 'superiorfrontal',
       'posteriorcingulate', 'rostralmiddlefrontal',
       'caudalmiddlefrontal', 'precentral', 'parstriangularis',
       'postcentral', 'parsopercularis', 'parsorbitalis', 'supramarginal',
       'superiortemporal', 'lateralorbitofrontal', 'middletemporal',
       'superiorparietal', 'fusiform', 'inferiorparietal',
       'inferiortemporal', 'Left Amy', 'Right EC', 'entorhinal',
       'temporalpole', 'Left PRC', 'Left CA2', 'Left CA1', 'CA1',
       'Left Cerebral White Matter', 'Left ITG inferior temporal gyrus',
       'Left PP planum polare', 'Left MTG middle temporal gyrus',
       'Left Hippocampus', 'Left Inf Lat Vent',
       'Left STG superior temporal gyrus', 'Left PIns posterior insula',
       'Left TTG transverse temporal gyrus',
       'Left MCgG middle cingulate gyrus',
       'Left MFG middle frontal gyrus',
       'Left OpIFG opercular part of the inferior frontal gyrus',
       'Left SMG supramarginal gyrus', 'insula', 'transversetemporal',
       'isthmuscingulate', 'paracentral', 'BA36',
       'Left FuG fusiform gyrus', 'Left TMP temporal pole', 'bankssts',
       'lateraloccipital', 'Right Cerebral White Matter',
       'Right MTG middle temporal gyrus', 'Right Thalamus Proper',
       'Right Putamen', 'Right Pallidum', 'Right Lateral Ventricle',
       'Right PCu precuneus', 'precuneus', 'Left CA3', 'Left DG',
       'Left Sub', 'Right Amy', 'Right Sub', 'Right CA1', 'Right PRC',
       'Left FRP frontal pole', 'Left MOrG medial orbital gyrus',
       'Left POrG posterior orbital gyrus',
       'Left LOrG lateral orbital gyrus', 'Left PrG precentral gyrus',
       'Left IOG inferior occipital gyrus', 'Left PoG postcentral gyrus',
       'Left Amygdala', 'Left PHG parahippocampal gyrus',
       'Right Amygdala', 'Right Hippocampus',
       'Right PHG parahippocampal gyrus', 'parahippocampal', 'DG',
       'Right PIns posterior insula', 'Right PP planum polare',
       'Right STG superior temporal gyrus', 'Right Ent entorhinal area',
       'Right GRe gyrus rectus', 'Right MOrG medial orbital gyrus',
       'Right AOrG anterior orbital gyrus',
       'Right OrIFG orbital part of the inferior frontal gyrus',
       'Right TrIFG triangular part of the inferior frontal gyrus',
       'Right OpIFG opercular part of the inferior frontal gyrus',
       'Right MCgG middle cingulate gyrus',
       'Right SMC supplementary motor cortex',
       'Right MFG middle frontal gyrus', 'Right AIns anterior insula',
       'Right CO central operculum', 'Right PrG precentral gyrus',
       'Right SMG supramarginal gyrus', 'Right PoG postcentral gyrus',
       'Left EC', 'Left MTL WM', 'misc', 'ERC', 'BA35', 'SUB',
       'Right FuG fusiform gyrus', 'Right ITG inferior temporal gyrus',
       'lingual', 'Right MTL WM', 'frontalpole',
       'caudalanteriorcingulate', 'Left PHC', 'Right DG', 'Right STG',
       'Left AOrG anterior orbital gyrus', 'Left AIns anterior insula',
       'Left Calc calcarine cortex', 'Left Cun cuneus',
       'Left AnG angular gyrus', 'Left PCgG posterior cingulate gyrus',
       'Left PCu precuneus', 'Left SPL superior parietal lobule',
       'Left LiG lingual gyrus', 'Left OFuG occipital fusiform gyrus',
       'Left Cerebellum Exterior', 'pericalcarine', 'cuneus',
       'Left Ent entorhinal area', 'Left Middle Temporal Gyrus',
       'Left Supramarginal Gyrus', 'Left CO central operculum',
       'Left MSFG superior frontal gyrus medial segment',
       'Left FO frontal operculum',
       'Left TrIFG triangular part of the inferior frontal gyrus',
       'Left OrIFG orbital part of the inferior frontal gyrus',
       'Left PT planum temporale', 'Left Lateral Ventricle',
       'Left PO parietal operculum', 'Right Inf Lat Vent',
       'Right SOG superior occipital gyrus', 'rostralanteriorcingulate',
       'PHC', 'Right ACgG anterior cingulate gyrus',
       'Right POrG posterior orbital gyrus', 'Left Putamen',
       'Right Middle Temporal Gyrus', 'Right AnG angular gyrus',
       'Left MFC medial frontal cortex',
       'Left SFG superior frontal gyrus',
       'Right SFG superior frontal gyrus',
       'Right MSFG superior frontal gyrus medial segment',
       'Right LiG lingual gyrus', 'Left Ventral DC', 'Left ACg',
       'Left ACgG anterior cingulate gyrus',
       'Left SMC supplementary motor cortex',
       'Left MPrG precentral gyrus medial segment',
       'Right MPrG precentral gyrus medial segment',
       'Right SPL superior parietal lobule',
       ' Left Cerebral White Matter', ' Left PrG precentral gyrus',
       ' Left PCgG posterior cingulate gyrus',
       ' Left PoG postcentral gyrus', ' Left Amygdala',
       ' Left STG superior temporal gyrus', ' Left Hippocampus',
       ' Left FuG fusiform gyrus', ' Left PHG parahippocampal gyrus',
       ' Left ITG inferior temporal gyrus',
       ' Left MTG middle temporal gyrus', ' Left AIns anterior insula',
       ' Left PIns posterior insula', ' Left MFG middle frontal gyrus',
       ' Left SFG superior frontal gyrus', ' Left FO frontal operculum',
       'sulcus', 'Left PCg', 'Left GRe gyrus rectus',
       'Right Accumbens Area', 'Right Caudate', 'Left MCg',
       'Right SCA subcallosal area', 'Left Thalamus Proper',
       'Left Caudate', 'Right IOG inferior occipital gyrus',
       'Right MOG middle occipital gyrus', 'Right PO parietal operculum',
       'Right PT planum temporale', 'Right FO frontal operculum',
       'Right TMP temporal pole', 'Right ACg', 'Right MCg', 'Right PHC',
       'Right PCg', 'Right PCgG posterior cingulate gyrus', 'Left SUB',
       ' Left CO central operculum', ' Left PO parietal operculum',
       ' Left MOG middle occipital gyrus', ' ', ' Right Amygdala',
       ' Right Cerebral White Matter', ' Right MTG middle temporal gyrus',
       ' Right Hippocampus', '', ' Right MFG middle frontal gyrus',
       ' Left MCgG middle cingulate gyrus',
       ' Left SMC supplementary motor cortex',
       ' Left MOrG medial orbital gyrus',
       ' Left AOrG anterior orbital gyrus',
       ' Left LOrG lateral orbital gyrus',
       ' Left TrIFG triangular part of the inferior frontal gyrus',
       ' Right GRe gyrus rectus', ' Right SMG supramarginal gyrus',
       ' Left SPL superior parietal lobule',
       ' Right MOrG medial orbital gyrus',
       ' Left ACgG anterior cingulate gyrus',
       ' Right STG superior temporal gyrus', ' Right Inf Lat Vent',
       ' Right FuG fusiform gyrus', ' Left PT planum temporale',
       ' Right CO central operculum', ' Right PoG postcentral gyrus',
       ' Right PrG precentral gyrus',
       ' Right SPL superior parietal lobule',
       ' Right MCgG middle cingulate gyrus',
       ' Right SFG superior frontal gyrus',
       ' Right OpIFG opercular part of the inferior frontal gyrus',
       ' Right IOG inferior occipital gyrus', ' Right AnG angular gyrus',
       ' Right PT planum temporale',
       ' Right TTG transverse temporal gyrus',
       ' Right ITG inferior temporal gyrus', ' Right Lateral Ventricle',
       ' Left Ent entorhinal area', ' Left Inf Lat Vent',
       ' Left TMP temporal pole', ' Left PP planum polare',
       ' Left GRe gyrus rectus', ' Left POrG posterior orbital gyrus',
       ' Right PHG parahippocampal gyrus', ' Right PIns posterior insula',
       ' Right AOrG anterior orbital gyrus', ' Right PP planum polare',
       ' Right AIns anterior insula', ' Right Putamen',
       ' Right TMP temporal pole', ' Right PCu precuneus',
       ' Right ACgG anterior cingulate gyrus',
       ' Right POrG posterior orbital gyrus',
       ' Right SMC supplementary motor cortex', ' Left PCu precuneus',
       ' Left SMG supramarginal gyrus', ' Left LiG lingual gyrus',
       ' Left MPrG precentral gyrus medial segment',
       ' Left AnG angular gyrus', ' Left Lateral Ventricle',
       ' Left IOG inferior occipital gyrus',
       ' Right Calc calcarine cortex', ' Right Cun cuneus',
       ' Left OCP occipital pole', ' Left SOG superior occipital gyrus',
       ' Right OCP occipital pole', ' Right SOG superior occipital gyrus',
       ' Left Cun cuneus', ' Left MFC medial frontal cortex',
       ' Left OrIFG orbital part of the inferior frontal gyrus',
       ' Left OpIFG opercular part of the inferior frontal gyrus',
       ' Left MSFG superior frontal gyrus medial segment',
       ' Left TTG transverse temporal gyrus',
       ' Right TrIFG triangular part of the inferior frontal gyrus',
       ' Right FO frontal operculum', ' Right MOG middle occipital gyrus',
       ' Right PO parietal operculum',
       ' Right LOrG lateral orbital gyrus', 'unknown',
       ' Left Cerebellum Exterior', ' Right Ent entorhinal area',
       ' Right MSFG superior frontal gyrus medial segment', 'Left MTG',
       'Right MTG', ' Right Ventral DC', ' Left FRP frontal pole',
       ' Right MPrG precentral gyrus medial segment', ' Left Putamen',
       ' Right Caudate', ' Right FRP frontal pole',
       ' Right MFC medial frontal cortex', ' Right LiG lingual gyrus',
       ' Left OFuG occipital fusiform gyrus',
       ' Right MPoG postcentral gyrus medial segment',
       ' Right PCgG posterior cingulate gyrus',
       ' Right OrIFG orbital part of the inferior frontal gyrus',
       ' Left Calc calcarine cortex', ' Right SCA subcallosal area',
       ' Left MPoG postcentral gyrus medial segment', ' Left Caudate',
       ' Left SCA subcallosal area'], dtype=object)
'''

'''
This it the colmplete list of regions I found in the FR1 dataset:
array(['Left CA1', 'Left PRC', 'Right DG', 'Right CA1', 'Right EC', 'CA1',
       'rostralmiddlefrontal', 'parstriangularis', 'superiortemporal',
       'precentral', 'postcentral', 'fusiform', 'inferiortemporal',
       'lingual', 'lateraloccipital', 'parahippocampal', 'supramarginal',
       'middletemporal', 'Left Amy', 'Left CA3', 'Right Amy', 'Right Sub',
       'caudalmiddlefrontal', 'lateralorbitofrontal', 'parsorbitalis',
       'temporalpole', 'frontalpole', 'superiorfrontal',
       'parsopercularis', 'precuneus', 'cuneus', 'superiorparietal',
       'inferiorparietal', 'bankssts', 'Right PRC', 'Left DG',
       'paracentral', 'posteriorcingulate', 'insula', 'isthmuscingulate',
       'Left DLPFC', 'entorhinal', 'Left Sub', 'pericalcarine',
       'Right MCg', 'BA36', 'Left Amygdala', 'Left Cerebral White Matter',
       'Left MTG middle temporal gyrus', 'Left FuG fusiform gyrus',
       'Left AnG angular gyrus', 'Left AIns anterior insula',
       'Left MFG middle frontal gyrus',
       'Left ITG inferior temporal gyrus', 'Left Putamen', 'SUB', 'DG',
       'Right Cerebral White Matter', 'Right Hippocampus',
       'Right Lateral Ventricle', 'Right MOG middle occipital gyrus',
       'Right AIns anterior insula', 'Right PIns posterior insula',
       'Right PO parietal operculum', 'Left Ent entorhinal area',
       'Left Hippocampus', 'Left Lateral Ventricle',
       'medialorbitofrontal', 'caudalanteriorcingulate',
       'Left TMP temporal pole', 'Left STG superior temporal gyrus',
       'Right MTG middle temporal gyrus', 'Right Thalamus Proper',
       'Right Putamen', 'Right Pallidum', 'Right PCu precuneus',
       'Left FRP frontal pole',
       'Left OpIFG opercular part of the inferior frontal gyrus',
       'Left MOrG medial orbital gyrus',
       'Left POrG posterior orbital gyrus',
       'Left LOrG lateral orbital gyrus', 'Left PrG precentral gyrus',
       'Left IOG inferior occipital gyrus', 'Left PoG postcentral gyrus',
       'Left PHG parahippocampal gyrus', 'Right Amygdala',
       'Right PHG parahippocampal gyrus', 'Left CA2', 'sulcus',
       'transversetemporal', 'Left Precentral Gyrus', 'Left EC',
       'Right PHC', 'Left Inf Lat Vent',
       'Left ACgG anterior cingulate gyrus',
       'Left SFG superior frontal gyrus',
       'Left SMC supplementary motor cortex',
       'Right MOrG medial orbital gyrus',
       'Right POrG posterior orbital gyrus',
       'Right LOrG lateral orbital gyrus', 'Right FO frontal operculum',
       'Right TrIFG triangular part of the inferior frontal gyrus',
       'Right OpIFG opercular part of the inferior frontal gyrus',
       'Right MCgG middle cingulate gyrus', 'Right PrG precentral gyrus',
       'Right MSFG superior frontal gyrus medial segment',
       'Right SFG superior frontal gyrus', 'Right FuG fusiform gyrus',
       'Right MFG middle frontal gyrus',
       'Right SMC supplementary motor cortex',
       'Right MPrG precentral gyrus medial segment',
       'Right SPL superior parietal lobule',
       'Right TTG transverse temporal gyrus',
       'Right PoG postcentral gyrus', 'Right FRP frontal pole',
       'Right PP planum polare', 'Right STG superior temporal gyrus',
       'Right Ent entorhinal area', 'Right GRe gyrus rectus',
       'Right AOrG anterior orbital gyrus',
       'Right OrIFG orbital part of the inferior frontal gyrus',
       'Right CO central operculum', 'Right SMG supramarginal gyrus',
       'Right Precentral Gyrus', 'Right MTL WM',
       'Left FO frontal operculum', 'Left TTG transverse temporal gyrus',
       'Right ITG inferior temporal gyrus', 'Right PT planum temporale',
       'BA35', 'misc', 'Left MTL WM', 'ERC', 'PHC',
       'Right AnG angular gyrus', 'Right TMP temporal pole',
       'Left MFC medial frontal cortex',
       'Right MFC medial frontal cortex',
       'Right ACgG anterior cingulate gyrus', 'rostralanteriorcingulate',
       'Left CO central operculum', 'Left PHC',
       'Left MCgG middle cingulate gyrus', 'Left PCu precuneus',
       'Left SMG supramarginal gyrus', 'Right STG',
       'Left AOrG anterior orbital gyrus', 'Left PP planum polare',
       'Left Calc calcarine cortex', 'Left Cun cuneus',
       'Left PCgG posterior cingulate gyrus',
       'Left SPL superior parietal lobule', 'Left LiG lingual gyrus',
       'Left OFuG occipital fusiform gyrus', 'Left Cerebellum Exterior',
       'Left PIns posterior insula', 'Right Inf Lat Vent',
       'Left Fusiform Gyrus WM',
       'Left MPrG precentral gyrus medial segment',
       'Left TrIFG triangular part of the inferior frontal gyrus',
       'Left Ventral DC', 'Right LiG lingual gyrus', 'Right Cun cuneus',
       'Right Calc calcarine cortex',
       'Left MSFG superior frontal gyrus medial segment',
       'Left OrIFG orbital part of the inferior frontal gyrus',
       'Left PT planum temporale', 'Left PO parietal operculum',
       'Right DLPFC', 'Right Caudal Middle Frontal Cortex',
       'Right Superior Frontal Gyrus', 'tail', 'Right ACg',
       'Left Caudal Middle Frontal Cortex',
       'Right SOG superior occipital gyrus',
       'Right PCgG posterior cingulate gyrus',
       'Left Middle Temporal Gyrus', 'Right Accumbens Area',
       'Right Caudate', 'Right CA3', 'Left Pallidum',
       'Left SOG superior occipital gyrus',
       'Right IOG inferior occipital gyrus',
       'Left MOG middle occipital gyrus', 'Right PCg',
       'Right Middle Temporal Gyrus', 'Left OCP occipital pole',
       'Left GRe gyrus rectus', 'Left MCg', 'Left Supramarginal Gyrus',
       'Left ACg', 'Left PCg', ' Left Cerebral White Matter',
       ' Left PrG precentral gyrus',
       ' Left PCgG posterior cingulate gyrus',
       ' Left PoG postcentral gyrus', ' Left Amygdala',
       ' Left STG superior temporal gyrus', ' Left Hippocampus',
       ' Left FuG fusiform gyrus', ' Left PHG parahippocampal gyrus',
       ' Left ITG inferior temporal gyrus',
       ' Left MTG middle temporal gyrus', ' Left AIns anterior insula',
       ' Left PIns posterior insula', ' Left MFG middle frontal gyrus',
       ' Left SFG superior frontal gyrus', ' Left FO frontal operculum',
       'CA2', 'Right SCA subcallosal area', 'Left SCA subcallosal area',
       'Left MPoG postcentral gyrus medial segment',
       ' Left TMP temporal pole', ' Left PP planum polare',
       ' Left CO central operculum', '', ' Left PT planum temporale', ' ',
       ' Left MOrG medial orbital gyrus',
       ' Left POrG posterior orbital gyrus', ' Left Cerebellum Exterior',
       ' Left OFuG occipital fusiform gyrus',
       ' Left IOG inferior occipital gyrus', ' Left Lateral Ventricle',
       ' Right MOrG medial orbital gyrus', ' Right Cerebral White Matter',
       ' Left ACgG anterior cingulate gyrus', ' Right Amygdala',
       ' Right STG superior temporal gyrus', ' Right Inf Lat Vent',
       ' Right MTG middle temporal gyrus', ' Right FuG fusiform gyrus',
       ' Right CO central operculum', ' Right PoG postcentral gyrus',
       ' Right PrG precentral gyrus',
       ' Right SPL superior parietal lobule',
       ' Right MCgG middle cingulate gyrus',
       ' Right MFG middle frontal gyrus',
       ' Left SMC supplementary motor cortex',
       ' Right SFG superior frontal gyrus', ' Left Thalamus Proper',
       ' Left MCgG middle cingulate gyrus',
       ' Left SPL superior parietal lobule', ' Left LiG lingual gyrus',
       ' Left Calc calcarine cortex', ' Left AnG angular gyrus',
       ' Left SMG supramarginal gyrus',
       ' Right OpIFG opercular part of the inferior frontal gyrus',
       ' Right IOG inferior occipital gyrus', ' Right AnG angular gyrus',
       ' Right PT planum temporale',
       ' Right TTG transverse temporal gyrus',
       ' Right ITG inferior temporal gyrus', ' Right Lateral Ventricle',
       ' Left Ent entorhinal area', ' Left Inf Lat Vent',
       ' Left AOrG anterior orbital gyrus',
       ' Left LOrG lateral orbital gyrus',
       ' Left TrIFG triangular part of the inferior frontal gyrus',
       ' Left GRe gyrus rectus', ' Left PCu precuneus',
       ' Right SMC supplementary motor cortex',
       ' Right Ent entorhinal area', ' Right TMP temporal pole',
       ' Right ACgG anterior cingulate gyrus',
       ' Right TrIFG triangular part of the inferior frontal gyrus',
       ' Right GRe gyrus rectus', ' Left MFC medial frontal cortex',
       ' Right PIns posterior insula', ' Right AIns anterior insula',
       'unknown',
       ' Left OpIFG opercular part of the inferior frontal gyrus',
       ' Right POrG posterior orbital gyrus',
       ' Right LOrG lateral orbital gyrus', ' Right Putamen',
       ' Right PHG parahippocampal gyrus',
       ' Right SMG supramarginal gyrus',
       ' Right AOrG anterior orbital gyrus', ' Right Hippocampus',
       ' Right PP planum polare', ' Right PCu precuneus',
       ' Left MPrG precentral gyrus medial segment', ' Left Cun cuneus',
       ' Left OrIFG orbital part of the inferior frontal gyrus',
       ' Left MSFG superior frontal gyrus medial segment',
       ' Left TTG transverse temporal gyrus',
       ' Right MOG middle occipital gyrus',
       ' Left MOG middle occipital gyrus', ' Right LiG lingual gyrus',
       ' Right Cerebellum Exterior', ' Right Calc calcarine cortex',
       ' Left PO parietal operculum',
       ' Right MSFG superior frontal gyrus medial segment',
       ' Right FO frontal operculum',
       ' Right MPrG precentral gyrus medial segment', ' Left Putamen',
       ' Right Caudate', 'Left MTG', 'Right MTG',
       ' Right PO parietal operculum',
       ' Left SOG superior occipital gyrus', ' Left OCP occipital pole',
       ' Right PCgG posterior cingulate gyrus',
       ' Right OrIFG orbital part of the inferior frontal gyrus',
       ' Left Caudate', ' Right MFC medial frontal cortex',
       ' Left FRP frontal pole', 'Amygdala', 'Caudate Tail',
       'Brodmann area 22', 'Brodmann area 28', 'Hippocampus',
       'Brodmann area 13', 'Brodmann area 21', 'Corpus Callosum',
       'Brodmann area 41_42', 'Brodmann area 11', 'Brodmann area 47',
       'Brodmann area 36', 'Brodmann area 20', 'Brodmann area 30',
       'Brodmann area 19', 'Brodmann area 37', 'Brodmann area 9',
       'Brodmann area 4_6', 'Brodmann area 46', 'Brodmann area 39',
       'Brodmann area 38', 'Brodmann area 35', 'Brodmann area 1_2_3_5',
       'Brodmann area 44', 'Brodmann area 40', 'Brodmann area 45',
       'Brodmann area 34', 'Brodmann area 43', 'Brodmann area 10',
       'Brodmann area 25', 'Brodmann area 27', 'Brodmann area 8',
       'Optic Tract', 'Putamen', 'Brodmann area 7', 'Brodmann area 18',
       'Lateral Globus Pallidus', 'Brodmann area 32', 'Brodmann area 24',
       'Brodmann area 31', 'Brodmann area 23', 'Brodmann area 29',
       'Medial Globus Pallidus', 'Brodmann area 17', 'nan',
       'Lateral Geniculum Body', 'Ventral Posterior Lateral Nucleus',
       'Hypothalamus'], dtype=object)
'''

'''
These are DLPFC relevant labels:
array(['superiorfrontal',
       'rostralmiddlefrontal',
       'caudalmiddlefrontal', 'Left DLPFC','Right DLPFC', 
      'Left MFG middle frontal gyrus','Right MFG middle frontal gyrus', 
       'Left SFG superior frontal gyrus','Right SFG superior frontal gyrus',
       ' Left MFG middle frontal gyrus',' Right MFG middle frontal gyrus',
       ' Left SFG superior frontal gyrus', ' Right SFG superior frontal gyrus',
       'Right Caudal Middle Frontal Cortex','Left Caudal Middle Frontal Cortex',
       'Brodmann area 46','Brodmann area 45' ,'Brodmann area 9'], dtype=object)
       
    
       
'''

