#include<iostream>
#include<stack>
using namespace std;
int prec(char c)
{
    switch( c)
    {
        case '+' : return 1;
        case '-' : return -1;
        case '*' : return 2;
         case '/' : return -2;
    }
}
int oper(int  a)
{
    switch(a)
    {
        case 1 : return '+';
        case -1: return '-';
        case  2: return '*';
         case -2: return '/';
    }
}
int main()
{
    stack <int> st;
    string s="a+b";
    string ans=" ";
    int t;
    int n=s.length();
    for(int i=0;i<n;i++){
        if(s[i]=='('){
        st.push(0);
          if(s[i]>='a'&&s[i]<='z'){
            ans+=s[i];
          }
        else
            if(st.empty()){
            st.push(prec(s[i]));
            (st.top()>prec(s[i])){
                int t=st.top;
                st.pop();
                char ch=oper(t);
                ans+=ch;
            }
        }}
        else{
        while(st.empty()&& abs(prec(s[i])<st.top)){
            st.pop();
                char ch=oper(t);
                ans+=ch;
        }}
        st.push(prec(s[i]));
    }
    cout<<"new expression "<<ans;
}