from sys import argv
def main():
    print("The Output:")
    file_path=argv[1]
    with open(file_path,'r') as f:
        line=f.readline()
        while line:
            if line=='u21':
                print line
                line=f.readline()
if __name__=='__main__':
    main()
