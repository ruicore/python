#include<string.h>

int is_palindrome(char *text)
{
    int i=0,n=strlen(text);
    for (i;i<=n/2;++i)
    {
        if (text[i]!=text[n-i-1])
        return 0;
    }
    return 1;
}