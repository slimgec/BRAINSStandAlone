from nipype.interfaces.base import CommandLine, CommandLineInputSpec, TraitedSpec, File, Directory, traits, isdefined, InputMultiPath, OutputMultiPath
import os
from nipype.interfaces.slicer.base import SlicerCommandLine


class BRAINSROIAutoInputSpec(CommandLineInputSpec):
    inputVolume = File(desc="The input image for finding the largest region filled mask.", exists=True, argstr="--inputVolume %s")
    outputROIMaskVolume = traits.Either(traits.Bool, File(), hash_files=False, desc="The ROI automatically found from the input image.", argstr="--outputROIMaskVolume %s")
    outputVolume = traits.Either(traits.Bool, File(), hash_files=False, desc="The inputVolume with optional [maskOutput|cropOutput] to the region of the brain mask.", argstr="--outputVolume %s")
    maskOutput = traits.Bool(desc="The inputVolume multiplied by the ROI mask.", argstr="--maskOutput ")
    cropOutput = traits.Bool(desc="The inputVolume cropped to the region of the ROI mask.", argstr="--cropOutput ")
    otsuPercentileThreshold = traits.Float(desc="Parameter to the Otsu threshold algorithm.", argstr="--otsuPercentileThreshold %f")
    thresholdCorrectionFactor = traits.Float(desc="A factor to scale the Otsu algorithm's result threshold, in case clipping mangles the image.", argstr="--thresholdCorrectionFactor %f")
    closingSize = traits.Float(desc="The Closing Size (in millimeters) for largest connected filled mask.  This value is divided by image spacing and rounded to the next largest voxel number.", argstr="--closingSize %f")
    ROIAutoDilateSize = traits.Float(desc="This flag is only relavent when using ROIAUTO mode for initializing masks.  It defines the final dilation size to capture a bit of background outside the tissue region.  At setting of 10mm has been shown to help regularize a BSpline registration type so that there is some background constraints to match the edges of the head better.", argstr="--ROIAutoDilateSize %f")
    outputVolumePixelType = traits.Enum("float", "short", "ushort", "int", "uint", "uchar", desc="The output image Pixel Type is the scalar datatype for representation of the Output Volume.", argstr="--outputVolumePixelType %s")
    numberOfThreads = traits.Int(desc="Explicitly specify the maximum number of threads to use.", argstr="--numberOfThreads %d")


class BRAINSROIAutoOutputSpec(TraitedSpec):
    outputROIMaskVolume = File(desc="The ROI automatically found from the input image.", exists=True)
    outputVolume = File(desc="The inputVolume with optional [maskOutput|cropOutput] to the region of the brain mask.", exists=True)


class BRAINSROIAuto(SlicerCommandLine):
    """title: Foreground masking (BRAINS)

category: Segmentation.Specialized

description: This program is used to create a mask over the most prominant forground region in an image.  This is accomplished via a combination of otsu thresholding and a closing operation.  More documentation is available here: http://wiki.slicer.org/slicerWiki/index.php/Documentation/4.1/Modules/ForegroundMasking.


version: 2.4.1

license: https://www.nitrc.org/svn/brains/BuildScripts/trunk/License.txt

contributor: Hans J. Johnson, hans-johnson -at- uiowa.edu, http://www.psychiatry.uiowa.edu

acknowledgements: Hans Johnson(1,3,4); Kent Williams(1); Gregory Harris(1), Vincent Magnotta(1,2,3);  Andriy Fedorov(5), fedorov -at- bwh.harvard.edu (Slicer integration); (1=University of Iowa Department of Psychiatry, 2=University of Iowa Department of Radiology, 3=University of Iowa Department of Biomedical Engineering, 4=University of Iowa Department of Electrical and Computer Engineering, 5=Surgical Planning Lab, Harvard)

"""

    input_spec = BRAINSROIAutoInputSpec
    output_spec = BRAINSROIAutoOutputSpec
    _cmd = " BRAINSROIAuto "
    _outputs_filenames = {'outputVolume':'outputVolume.nii','outputROIMaskVolume':'outputROIMaskVolume.nii'}
