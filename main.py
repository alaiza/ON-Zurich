import sys
import argparse
import logging
import logging.config
from logging.handlers import TimedRotatingFileHandler
from os import listdir
from os.path import isfile, join
from File_Processor.file_manager import FileManager
import datetime



def main():
    try:
        logger = specific_logger()
        logger.info("Starting execution")
        parser = build_argument_parser()
        arguments = vars(parser.parse_args())
        relative_path = arguments.get('relative_path')
        output_path = arguments.get('output_path')
        Lfiles = getListOfFiles(relative_path, logger)
        file_dealer = FileManager(relative_path, Lfiles, logger)
        file_dealer.run()
        LInfo = file_dealer.getInfo()
        logger.info('{0} files correctly parsed'.format(str(len(LInfo))))
        logger.info('writing info in path {0}'.format(output_path))
        writeOutputFile(output_path,LInfo)
        logger.info('File was written')

    except Exception, ex:
        logger.critical("Something went so bad")
        print ex

def writeOutputFile(output_path,LInfo):
    now = datetime.datetime.now()
    with open('{0}output-{1}.yml'.format(output_path, now.strftime("%Y-%m-%d_%H-%M-%S")), 'w') as f:
        for item in LInfo:
            f.write("%s\n" % item)


def getListOfFiles(relativepath, logger):
    onlyfiles = [f for f in listdir(relativepath) if isfile(join(relativepath, f))]
    Lcleanedfiles = []
    for a in onlyfiles:
        if a[-4:] == '.sql':
            Lcleanedfiles.append(a)
    if len(Lcleanedfiles)>=1:
        logger.info('Files that will be processed:')
        for file in onlyfiles:
            logger.info(""">> {0}""". format(file))
        return Lcleanedfiles
    else:
        logger.warn("""
        We couldnt find any file on this path: {0}
        please check if the files are correctly located
        
        ...forcing exit
        """.format(relativepath))
        sys.exit(0)


def build_argument_parser():
    parser = argparse.ArgumentParser(description='Test_Zurich_project_parser')
    parser.add_argument("--relative_path", required=False, type=str, default='./sql_scripts/', help="""
    Provide the relative path where the files are located
    Default: ./sql_scripts/
    """)
    parser.add_argument("--output_path", required=False, type=str, default='./output/', help="""
        Provide the relative path where the output file will be located
        Default: ./output/
        """)
    return parser


def specific_logger():
    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')

    handler = TimedRotatingFileHandler('logs/logfile.log',
                                       when='midnight',
                                       backupCount=10)
    handler.setFormatter(formatter)
    logger = logging.getLogger(__name__)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger


if __name__ == "__main__":
    main()

