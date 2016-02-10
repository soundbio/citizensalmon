// IterationPCA.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <iostream>

using namespace std;

void Usage()
{
    cerr << _T("Usage: IterationPCA [-g <genepop data filepath> | -f <fasta data filepath> ]") << endl;
}

int _tmain(int argc, _TCHAR* argv[])
{
    _TCHAR* arg = *argv;
    _TCHAR* ptr = arg;

    //while(arg != argv + argc)
    {
        ptr = arg;
        if (*ptr == _T('-'))
            ptr++;
            switch(*ptr)
            {
                case _T('g'):
                    // genepop
                    arg++;

                    break;
                case _T('f'):
                    // fasta
                    break;
                default:
                    Usage();
            }
    }

	return 0;
}

