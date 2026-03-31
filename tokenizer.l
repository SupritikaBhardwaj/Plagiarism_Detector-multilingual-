%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXTOKENS 10000

char tokens1[MAXTOKENS][50];
char tokens2[MAXTOKENS][50];

int t1=0;
int t2=0;
int file_no=1;

void store_token(char *tok)
{
    if(file_no==1)
    {
        strcpy(tokens1[t1++],tok);
    }
    else
    {
        strcpy(tokens2[t2++],tok);
    }
}
%}

ID      [a-zA-Z_][a-zA-Z0-9_]*
NUM     [0-9]+
OP      [+\-*/%=<>!&|^]+
DELIM   [(){};,.\[\]]

%%

{ID}        { store_token(yytext); }
{NUM}       { store_token(yytext); }
{OP}        { store_token(yytext); }
{DELIM}     { store_token(yytext); }

[ \t\n]+    ;

.           { store_token(yytext); }

%%

int lcs()
{
    int dp[1000][1000];

    for(int i=0;i<=t1;i++)
        for(int j=0;j<=t2;j++)
            dp[i][j]=0;

    for(int i=1;i<=t1;i++)
    {
        for(int j=1;j<=t2;j++)
        {
            if(strcmp(tokens1[i-1],tokens2[j-1])==0)
                dp[i][j]=dp[i-1][j-1]+1;
            else
                dp[i][j]=(dp[i-1][j]>dp[i][j-1])?dp[i-1][j]:dp[i][j-1];
        }
    }

    return dp[t1][t2];
}

int main(int argc,char *argv[])
{

    if(argc<3)
    {
        printf("Usage: %s file1 file2\n",argv[0]);
        return 1;
    }

    FILE *f1=fopen(argv[1],"r");
    FILE *f2=fopen(argv[2],"r");

    if(!f1 || !f2)
    {
        printf("Error opening files\n");
        return 1;
    }

    yyin=f1;
    file_no=1;
    yylex();

    yyin=f2;
    file_no=2;
    yylex();

    int match=lcs();

    float similarity=(2.0*match)/(t1+t2)*100;

    printf("Total Tokens File1: %d\n",t1);
    printf("Total Tokens File2: %d\n",t2);
    printf("Matching Tokens: %d\n",match);
    printf("Token Similarity: %.2f%%\n",similarity);

    fclose(f1);
    fclose(f2);

    return 0;
}