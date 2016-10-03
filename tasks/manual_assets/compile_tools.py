from tasks.common import *

def task_compile_tools():
    return {
        'actions': [None],
        'task_dep': [
            'compile_python',
            'compile_perl',
            'compile_r',
            'compile_bwa',
            'compile_htslib',
            'compile_samtools',
            'compile_bcftools',
            'compile_bedtools',
            'compile_gatk'
        ]
    }

def task_compile_python():
    return {
        'actions': [
            cmd('make', cwd=PYTHON_ROOT)
        ],
        'targets': [os.path.join(PYTHON_ROOT, 'bin', 'python')],
        'uptodate': [True]
    }

def task_compile_perl():
    return {
        'actions': [
            cmd('yes | ./configure.sh && make', cwd=PERL_ROOT)
        ],
        'targets': [os.path.join(PERL_ROOT, 'perl')],
        'uptodate': [True]
    }

def task_compile_r():
    return {
        'actions': [
            cmd('./configure && make', cwd=R_ROOT)
        ],
        'targets': [os.path.join(R_ROOT, 'bin', 'R')],
        'uptodate': [True]
    }

def task_compile_bwa():
    return {
        'actions': [
            cmd('./configure && make', cwd=BWA_ROOT)
        ],
        'targets': [os.path.join(BWA_ROOT, 'bwa')],
        'uptodate': [True]
    }

def task_compile_htslib():
    return {
        'actions': [
            cmd('make', cwd=HTSLIB_ROOT)
        ],
        'targets': [os.path.join(HTSLIB_ROOT, 'htsfile')],
        'uptodate': [True]
    }

def task_compile_samtools():
    return {
        'actions': [
            cmd('make', cwd=SAMTOOLS_ROOT)
        ],
        'targets': [os.path.join(SAMTOOLS_ROOT, 'samtools')],
        'uptodate': [True]
    }

def task_compile_bcftools():
    return {
        'actions': [
            cmd('make', cwd=BCFTOOLS_ROOT)
        ],
        'targets': [os.path.join(BCFTOOLS_ROOT, 'bcftools')],
        'uptodate': [True]
    }

def task_compile_bedtools():
    return {
        'actions': [
            cmd('make', cwd=BEDTOOLS_ROOT)
        ],
        'targets': [os.path.join(BEDTOOLS_ROOT, 'bedtools')],
        'uptodate': [True]
    }

def task_compile_gatk():
    return {
        'actions': [
            cmd('''
            mvn verify -P\!queue\
            && GATK_JAR=`readlink -f target/GenomeAnalysisTK.jar`\
            && unlink target/GenomeAnalysisTK.jar\
            && mv $GATK_JAR ./GenomeAnalysisTK.jar\
            && bash -O extglob -c 'rm -rf !(GenomeAnalysisTK.jar)'
            ''', cwd=GATK_ROOT)
        ],
        'targets': [os.path.join(GATK_ROOT, 'gatk')],
        'uptodate': [True]
    }