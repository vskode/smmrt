from pathlib import Path
import soundfile as sf

def save_resampled_file(path, target_sr, target_folder, file_ending='.wav', 
                        **kwargs):
    """
    Save a file with a different sample rate compared to the original. 
    Key word arguments can be passed so that the a offset or duration can
    be specified (to get rid of a audio check in every file for example). 

    Args:
        path (str): path to root directory containing the files
        target_sr (int): target sample rate
        target_folder (str): name of folder where files should be stored
        file_ending (str, optional): Defaults to '.wav'.
    """
    Path(path).joinpath(target_folder).mkdir(exist_ok=True)
    
    files = list(Path(path).glob(f'*{file_ending}'))
    
    for i, file in enumerate(files):
        audio, sr = load_audio(file, **kwargs)
        sf.write(file.parent.joinpath(target_folder)
                 .joinpath(file.stem+file.suffix), audio, target_sr)
        
        # update progress
        print(r'Resampling file {}/{} from {} Hz to {} Hz | {:.3f}% completed'
                .format(i, len(files), sr, target_sr, i/len(files)*100), 
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
        audio, sr = sf.read(file, **kwargs)
        return audio, sr
    except Exception as e:
        print(f"{file} is corrupted. Moving on to next file", e)
    
if __name__ == '__main__':
    path = r'D:\5122\5122'
    path = r'/media/vincent/TOSHIBA EXT/5122/5122'
    save_resampled_file(path, target_sr=2000, target_folder='resampled_2kHz')