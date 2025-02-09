import sys
from PIL import Image

    
def main():
    try:
        path = sys.argv[1]

        with Image.open(path) as img:
            img.save(path[:-4] + ".ico", format='ICO')
        
    except IndexError:
        print("Usage: png2ico path_to_png_file")
        
    except Exception as e:
        print(e)
        
        
if __name__ == "__main__":
    main()
