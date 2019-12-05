//#include<bits/stdc++.h>
#include <cstdio>
#include <iostream>
#include <vector>
#include <algorithm>
#include <cstring>
#include <string>
using namespace std;
/*
���밴�޴��ڽӱ�;޴�Ȩֵ������� 
���������ֲ�
*/
// ȫ�ֱ��� 
vector<int>E1[100005];
vector<int>E2[100005];
double Mat[1005][1005];// ͼ1�ĵ�i�����ͼ2�ĵ�j����ı�Ȩ 
int N1,N2;
int Match[1005];// ͼ1�ĵ�i����ƥ����ͼ2���ĸ��� 
double finalres;
double alpha;
// ÿ�εı��� 
const int MAXN = 1005;
const int INF = 0x3f3f3f3f;
double weight[MAXN][MAXN];
double eleft[MAXN];
double eright[MAXN];
bool okleft[MAXN];
bool okright[MAXN];
int match[MAXN];// i-th right match / -1 
double slack[MAXN];
int N;
bool dfs(int lnode){
    okleft[lnode] = true;
    for (int rnode = 0; rnode < N; ++rnode) {
        if (okright[rnode]) continue;
        double gap = eleft[lnode] + eright[rnode] - weight[lnode][rnode];
        if (gap == 0) {
            okright[rnode] = true;
            if (match[rnode] == -1 || dfs( match[rnode] )) {
                match[rnode] = lnode;
                return true;
            }
        } else slack[rnode] = min(slack[rnode], gap);
    }
    return false;
}
double KM(){
    memset(match, -1, sizeof match);
    fill(eright,eright+MAXN,0);
    for (int i = 0; i < N; ++i) {
        eleft[i] = weight[i][0];
        for (int j=1;j<N;++j)eleft[i] = max(eleft[i], weight[i][j]);
    }
    for (int i = 0; i < N; ++i) {
        fill(slack, slack + N, INF);
        while (1) {
            memset(okleft, false, sizeof okleft);
            memset(okright, false, sizeof okright);
            if (dfs(i)) break;
            double d = INF;
            for (int j = 0; j < N; ++j) if (!okright[j]) d = min(d, slack[j]);
            for (int j = 0; j < N; ++j) {
                if (okleft[j]) eleft[j] -= d;
                if (okright[j]) eright[j] += d;
                else slack[j] -= d;
            }
        }
    }
    double res=0;
    // �Ҳ��i����ƥ�䵽�����ĸ��� 
    for(int i=0;i<N;++i)res+=weight[match[i]][i];
    return res;
}
double calc(int root1,int root2){
	vector<int>floor1;
	vector<int>floor2;
	if(root1!=-1)for(int i=0;i<E1[root1].size();i++)floor1.push_back(E1[root1][i]);
	if(root2!=-1)for(int i=0;i<E2[root2].size();i++)floor2.push_back(E2[root2][i]);
	if(floor1.size()==0&&floor2.size()==0)return 0;
	int n;
	/*
	���������⣬������������N-N�ģ�����Ҫ��������㣬ƥ��ֵ����-1��
	*/
	n=N=max(floor1.size(),floor2.size());
	for(int i=0;i<n;i++)for(int j=0;j<n;j++)weight[i][j]=-1;
	for(int i=0;i<floor1.size();i++)for(int j=0;j<floor2.size();j++)weight[i][j]=-Mat[floor1[i]][floor2[j]];
//	int extra=N-min(floor1.size(),floor2.size());
	// �ݹ�������㣬��Ȼ��ʵ��̫���� 
//	finalres+=KM()*ratio/n;
	KM();
	vector<int>matchL;
	vector<double>res;
	for(int i=0;i<n;i++)matchL.push_back(match[i]);
	for(int i=0;i<n;i++)res.push_back(0);
	for(int i=0;i<n;i++)res[matchL[i]]=weight[match[i]][i];
	for(int i=0;i<n;i++){
		if(i>=(int)floor2.size()){
			res[matchL[i]]+=calc(floor1[matchL[i]],-1);
			continue;
		}else if(matchL[i]>=(int)floor1.size()){
			res[matchL[i]]+=calc(-1,floor2[i]);
			continue;
		}else{
			Match[floor1[matchL[i]]]=floor2[i];
			res[matchL[i]]+=calc(floor1[matchL[i]],floor2[i]);
		}
	}
	double ans=0;
	for(int i=0;i<n;i++)ans+=res[i];
	ans=ans*alpha/n;
	return ans;
//	for(int i=0;i<floor1.size();i++)
//		if(Match[floor1[i]]!=-1&&E1[floor1[i]].size()!=0&&E2[Match[floor1[i]]].size()!=0)
//			calc(floor1[i],Match[floor1[i]],ratio*alpha);

//	for(int i=0;i<N;i++){
//		if(match[i]>=(int)floor1.size())continue;
//		Match[floor1[match[i]]]=floor2[i];
//	}
//	for(int i=0;i<floor1.size();i++)
//		if(Match[floor1[i]]!=-1&&E1[floor1[i]].size()!=0&&E2[Match[floor1[i]]].size()!=0)
//			calc(floor1[i],Match[floor1[i]],ratio*alpha);
//    while (~scanf("%d", &N)) {
//        for (int i = 0; i < N; ++i)
//            for (int j = 0; j < N; ++j){
//                scanf("%lf", &weight[i][j]);
//            	weight[i][j]=-weight[i][j];
//			}
//        printf("%.0f\n", KM());
//    }
}
/*
˥������q����a1=1-q
����:1/2,1/4,.... 
*/
void solve(){
	/*
	�� root �� 0
	����һ��ĸ�ڵ㣺
		��ȡһ��
		KMƥ��
		��ȫ�ּ�¼ƥ��
		��ĸ�ڵ�ֱ����ÿ��ƥ���ݹ���� 
	*/
	finalres=0;
	alpha=0.5;
	for(int i=0;i<N1;i++)Match[i]=-1;
	// ������¹�ʽ
	// aV1 + aqV2 + aq^2V2
	//=a(q(V1+q(V2+ ... )))/q
	cout<<-calc(0,0)/alpha*(1-alpha)<<endl;
//	cout<<-finalres<<endl;
}
int main(){
	freopen("a.txt","r",stdin);
	int nedge,tu,tv;
	cin>>N1>>nedge;
	while(nedge--){cin>>tu>>tv;E1[tu].push_back(tv);}
	cin>>N2>>nedge;
	while(nedge--){cin>>tu>>tv;E2[tu].push_back(tv);}
//	for(int i=0;i<N1;i++){
//		int k=0,temp;cin>>k;
//		while(k--){cin>>temp;E1[i].push_back(temp);}
//	}
//	cin>>N2;
//	for(int i=0;i<N2;i++){
//		int k=0,temp;cin>>k;
//		while(k--){cin>>temp;E2[i].push_back(temp);}
//	}
	for(int i=0;i<N1;i++)
		for(int j=0;j<N2;j++)
			cin>>Mat[i][j];
	solve();
    return 0;
}
