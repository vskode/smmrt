from pathlib import Path
import soundfile as sf
import librosa as lb
import re
import datetime as dt

def create_dir_from_date(file, target_folder):
    """
    Create a directory tree for year, month and day, depending on the file
    name. 

    Parameters
    ----------
    file : pathlib.Path object
        file path
    target_folder : str
        folder for resampled files

    Returns
    -------
    pathlib.Path object
        directory to save file in
    """
    datetime_str = re.findall('[0-9]+', file.stem)[-1]
    date = dt.datetime.strptime(datetime_str, '%y%m%d%H%M%S').date()
    new_dir = file.parent.joinpath(target_folder) \
                .joinpath(str(date.year)) \
                .joinpath(str(date.month)) \
                .joinpath(str(date.day))
    new_dir.mkdir(exist_ok=True, parents=True)
    return new_dir
    
def save_resampled_file(path, target_sr, target_folder, file_ending='.wav', 
                        reorder_files=False, **kwargs):
    """
    Save a file with a different sample rate compared to the original. 
    Key word arguments can be passed so that the a offset or duration can
    be specified (to get rid of a audio check in every file for example). 

    Args:
        path (str): path to root directory containing the files
        target_sr (int): target sample rate
        target_folder (str): name of folder where files should be stored
        file_ending (str, optional): Defaults to '.wav'.
        reorder_files (bool, optional): Defaults to False.
    """    
    files = list(Path(path).glob(f'*{file_ending}'))
    
    for i, file in enumerate(files):
        audio, sr = load_audio(file, **kwargs)
        audio = lb.resample(audio, orig_sr=sr, target_sr=target_sr)
        if reorder_files:
            new_dir = create_dir_from_date(file, target_folder)
        else:
            new_dir = file.parent.joinpath(target_folder)
        sf.write(new_dir.joinpath(file.stem+file.suffix), audio, target_sr)
        
        # update progress
        print(r'Resampling file {}/{} from {} Hz to {} Hz | {:.3f}% completed'
                .format(i+1, len(files), sr, target_sr, (i+1)/len(files)*100), 
                end='\r')

def load_audio(file, **kwargs):
    """
    Load audio file, print error if file is corrupted but continue with next 
    file. 

    Args:
        file (pathlib.Path): file path

    Returns:
        tuple: audio as array and samplerate
    """
    try:
        audio, sr = lb.load(file, sr=None, **kwargs)
        return audio, sr
    except Exception as e:
        print(f"{file} is corrupted. Moving on to next file", e)
    
if __name__ == '__main__':
    # path = r'D:\5122\5122'
    path = r'/media/vincent/TOSHIBA EXT/5122/5122'
    save_resampled_file(path, target_sr=2000, target_folder='resampled_2kHz', 
                        reorder_files=True)