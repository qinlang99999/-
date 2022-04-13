#include<iostream>
#include<string>
#include<sstream>
#include <iomanip>
using namespace std;
string Qinlang(string Qinlang, int times) {
	string bb("");
	for (int i = 0;i < times;i++) {
		bb += Qinlang[i];
	}
	for (int i = times + 1;;i++) {
		if (Qinlang[i] == 'e') {
			break;
		}
		bb += Qinlang[i];
	}
	string ZhangQiman;
	int love;
	for (int i = 0;;i++) {

		if (Qinlang[i] == 'e') {
			love = i;
			break;
		}
	}
	for (int i = love + 1;i < Qinlang.size();i++) {
		ZhangQiman += Qinlang[i];
	}
	stringstream strs;
	strs << ZhangQiman;
	strs >> love;
	if ((times + love) <= 0) {
		for (int i = 0;i < 1 - (times + love);i++) {
			bb = '0' + bb;
		}
		times = 1;
	}
	else if ((times + love) >= bb.size()) {
		int dddd = bb.size();
		for (int i = 0;i < times + love - dddd;i++) {
			bb += '0';
		}
		times = -1;
	}
	else {
		times += love;
	}
	string cc = "";
	if (times >= 0) {

		for (int i = 0;i < times;i++) {
			cc += bb[i];
		}
		cc += ".";
		for (int i = times;i < bb.size();i++) {
			cc += bb[i];
		}
		for (int i = 0;i < 6 - (bb.size() - times);i++) {
			cc += '0';
		}
	}
	else {
		cc = bb + ".000000";
	}
	return cc;
}
int main() {
	string aaa;
	int aa = 0;
	getline(cin, aaa);
	for (int i = 0;i < aaa.size();i++) {
		if ((aaa[i] == '.') || (aaa[i] == 'e')) {
			aa = i;
			break;
		}
	}
	if (aaa[aa] == 'e') {
		string bbbba("");
		for (int i = 0;i < aa;i++) {
			bbbba += aaa[i];
		}
		bbbba += ".";
		for (int i = aa;i < aaa.size();i++) {
			bbbba += aaa[i];
		}
		aaa = bbbba;
	}
	string bb(Qinlang(aaa, aa));
	const char* ainizqm = bb.c_str();
	float really = stof(ainizqm);
	cout << setiosflags(ios::fixed) << setprecision(6);
	cout << really;
}