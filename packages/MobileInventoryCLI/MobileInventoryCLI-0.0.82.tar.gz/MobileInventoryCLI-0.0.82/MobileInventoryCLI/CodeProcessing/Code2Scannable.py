import csv,os,sys
from barcode import EAN8,UPCA
from barcode.writer import ImageWriter
from pathlib import Path
from colored import Fore,Style
import upcean
import shutil
class Code2Scannable:
    def __init__(self,filename=Path("scannable.csv"),):
        if filename == None:
            while True:
                f=input(f"{Fore.green_yellow}File Containing UPCA/UPCE\ncodes to be encoded/converted for \nuse with {Style.bold}{Fore.magenta}Safeway App[or q=Quit]!{Style.reset}: ")
                if f.lower() == 'q':
                    exit("user quit... nothing will be written!")
                a=Path(f)
                if a.exists() and a.is_file():
                    self.filename=a
                    break   
        else:
            self.filename=filename
        self.dir=Path("collected")
        if not self.dir.exists():
            self.dir.mkdir()
        else:
            shutil.rmtree(self.dir)
            self.dir.mkdir()
        with self.filename.open("r") as ifile:
            reader=csv.reader(ifile,delimiter=',')
            duplicates=0
            for num,line in enumerate(reader):
                if num > 0:
                    for c in [UPCA,]:
                        print(c,line)
                        try:
                            if len(line) >= 1:
                                if len(line[0]) >= 11:
                                    x=c(line[0],writer=ImageWriter())
                                    print(f"{Fore.green}{x}{Style.reset} {Fore.red}{num}{Style.reset}")
                                    p=self.dir/Path(line[0]+".png")
                                    if p.exists():
                                        duplicates+=1
                                        print(f"{Fore.yellow}Overwriting {p}{Style.reset}{Fore.green_yellow} {duplicates}{Style.reset}")

                                    x.save(str(self.dir/Path(line[0])))
                                    break
                                elif len(line[0]) == 8:
                                    nc=upcean.convert.convert_barcode(outtype="upca",upc=line[0],intype="upce")
                                    sfpath=self.dir/Path(f'{line[0]}-{nc}.png')
                                    x=c(nc,writer=ImageWriter())
                                    print(f"{Fore.green}{x}{Style.reset} {Fore.red}{num}{Style.reset}")
                                    p=self.dir/Path(line[0]+"-{nc}"+".png")
                                    if p.exists():
                                        duplicates+=1
                                        print(f"{Fore.yellow}Overwriting {p}{Style.reset}{Fore.green_yellow} {duplicates}{Style.reset}")

                                    x.save(str(self.dir/Path(line[0]+f"-{nc}")))
                                    break
                                else:
                                    print(f"{Fore.red}{Style.bold}Unsupported Code Len {len(line[0])}{Style.reset}")
                        except Exception as e:
                            print(e,c,line)
if __name__ == "__main__":
    Code2Scannable()
