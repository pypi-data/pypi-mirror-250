import argparse
import os
import time
from .utils import scSPRITE,sn_m3c,scNano
from .utils import help
from .utils import tools as tl

from multiprocessing import Process, Queue, Pool, Manager
from .utils.scaffold import *
from .utils.assembly import *
from .utils.download import make_index
import logging
Path = os.getcwd()
print(Path)
tech = {
        'scSPRITE':scSPRITE,
        
        'sn_m3c':sn_m3c,
        'scNano':scNano
       }

def run_pipeline(opt):
    # 转化为字典
    opt = dict(opt.__dict__)
    opt['running_path'] = Path

    # 先创建output文件夹，没有则创建，有则退出;然后移到该工作目录下面
    tl.make_workflow(opt['output'])
    os.chdir(opt['output'])

    # 然后判断是不是到底有多少个样本，如果是一个样本，那么就直接运行，如果是多个样本，那么就要用多进程来运行
    opt, fastq_log = tl.count_sample(opt)

 

    # 判断index是否存在
    tl.check_index(opt)
    tl.check_enzyme(opt)

    tl.get_enzyme_bed(opt)

    opt = tl.parser_fa_and_chrom_size(opt)

    # 查询是什么物种
    opt['species'] = tl.parse_species(opt)
    
    # print(opt)
    
    
    # gobal logging
    log_out = tl.log_(opt)
    os.chdir(opt['output'])

    if len(fastq_log) <= opt['worker']:
        print('*****num of worker is more than num of sample*****')
        p = Pool(opt['worker'])
        for fq in fastq_log:
            # 根据type来允许不同的流程
           run_exec(opt['type'],opt, fq,log_out)
        p.close()
        p.join()
    else:
        print('*****num of worker is less than num of sample*****')
        divide_list = []
        for i in range(0, len(fastq_log), opt['worker']):
            divide_list.append(fastq_log[i:i + opt['worker']])

        # logging batch 
        log_out.debug('divide_list:{}'.format(len(divide_list)))

        for i,val in enumerate(divide_list):
            p = Pool(len(val))
            for j,fq in enumerate(val):
                log_out.debug('%s || %s.....Dealing fq: %s \n' % (i*opt['worker']+ j,len(fastq_log),fq))
               
            
                p.apply_async(run_exec, args=(opt['type'],opt, fq,log_out))
                
            p.close()
            p.join()
            log_out.debug('Batch %s done || %s \n' % (i,len(divide_list)/opt['worker']))
    log_out.debug('All done || %s \n' % (len(fastq_log)))

def run_exec(type_,opt, fq,log_out):
    if type_ == 'sn_m3c' or type_ == 'scSPRITE' or type_ == 'scNano':
        if type_ == 'sn_m3c' and opt['aligner'] == 'bwa':
            log_out.debug('sn_m3c only support bowtie2')
            print('sn_m3c only support bowtie2')
            return
 
        exec(type_ + '.pp' + '(opt=opt,fastq=fq,log_out=log_out)')
    else:
        assembly(type_,opt, fq,log_out)

    






def main():
    parser = argparse.ArgumentParser()
    subparsers1 =  parser.add_subparsers()
    count = subparsers1.add_parser('count', help='to dealing with different type of hic from fastq')
    count.add_argument('-o', '--output',required=True , help='save path')
    count.add_argument('-f', '--fastq', required=True, help='fastq_dir, run all if -s is not be specfied',)
    count.add_argument('--logging', help='logging', default='./log.log')
    count.add_argument('-t', '--type',
                        choices=['scHic', 'snHic','sciHic','scSPRITE','dipC','sn_m3c','HIRES', 'scNano'],
                         help='type of hic',required=True )
    count.add_argument('-e', '--enzyme', help='enzyme,mboi',type=str,required=True)
    count.add_argument('-r', '--resolution', help='resoluation', default=10000)
    count.add_argument('-i', '--index', help='bwa fa file/bowtie fa file', required=True )
    count.add_argument('-s', '--sample', help='sample to count if needed, you should provide the txt file where each line is a sample name',
                        default=None)
    count.add_argument('--exist-barcode' , action='store_true', help='if the tech has barcode, you should add this parameter')
    count.add_argument('--qc', type=int, default=0, help='samtools view to  qc')
    count.add_argument('--add-columns', default='mapq', help=help.help['add_columns'])
    count.add_argument('--thread', help='threads for processing the data', type=int, default=10)
    count.add_argument('--worker', help='processiing the data on num of worker simultaneously', type=int, default=1)
    count.add_argument('--select', help=help.help['select'],default="mapq1>=30 and mapq2>=30")
    count.add_argument('--max-mismatch', help=help.help['max_mismatch'], type=int, default=3)
    count.add_argument('-a', '--aligner', default='bowtie2', choices=['bwa', 'bowtie2'], help='aligner')
    count.add_argument('--repeat-masker', help='repeat masker(bed file) for scSPRITE', default=None)
    count.add_argument('--sprite-config', help='sprite-config', default=None)
    count.add_argument('--scNano-barcode',default=None,
                        help='scNano barcode for PCR and TN5, which should be stored in a folder and named as TN5.txt and PRC,index.txt.txt respectively')
    count.add_argument('--zoomify-res', help='zoomify',type=str, default='10000,40000,100000,500000')
    count.set_defaults(func='count')

    index = subparsers1.add_parser('index', help='to make bowtie2/bwa index and enzyme bed')
    index.add_argument('-g', '--genome', help='choose from hg38,hg19,mm10,mm9', choices=['hg38','hg19','mm10','mm9'],required=True)
    index.add_argument('-a', '--aligner', help='choose from bowtie2, bwa',choices=['bowtie2', 'bwa'], required=True)
    index.add_argument('-p', '--path', help='path to save index', required=True)
    index.add_argument('-e', '--enzyme', help='enzyme to digest, you can input multiple enzyme,like: MboI,DpnII,BglII',required=True)
    index.set_defaults(func='index')
    args = parser.parse_args()


    try:
        args.func
    except:
        print('scihickit: a tool for dealing with single-cell Hi-C')
        print('usage: scihickit <command> [<args>]')
        print('Commands: index, count, for more information, please use scihickit <command> -h')
        sys.exit()

    if  args.func == 'count':
        run_pipeline(args)
    elif args.func == 'index':
        make_index(args.path, args.genome, args.aligner, args.enzyme)
    else:
         parser.print_help()

        
if __name__ == '__main__':
    Time = time.time()
    main()
    print('=============time spen ', time.time() - Time, '===================')