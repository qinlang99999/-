#include<iostream>
#include<string>
using namespace std;
string insert(string aaaa, string c) {
	int aa = 0;
	for (int i = 0;i < aaaa.size();i++) {
		if (aaaa[i] > c[0]) {
			aa = i;
			break;
		}
		if (i == aaaa.size() - 1) {
			aa = aaaa.size();
		}
	}
	string bb("");
	for (int i = 0;i < aa;i++) {
		bb += aaaa[i];
	}
	bb += c[0];
	for (int i = aa;i < aaaa.size() + 1;i++) {
		bb += aaaa[i];
	}
	return (bb);
}
int main() {
	string aaa;
	string bbb;
	getline(cin, aaa);
	getline(cin, bbb);
	cout << insert(aaa, bbb);
}