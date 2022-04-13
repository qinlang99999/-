#include<iostream>
using namespace std;
class Matrix {
    friend int** operator+=(const Matrix aq, const Matrix bq);
    friend int** operator*=(Matrix aq, Matrix bq);
    int ae, be;
    int** ce;
public:
    Matrix(int a = 0, int b = 0) :
        ae(a), be(b), ce(f1()) {
    };
    int f2(int p, int q) { return ce[p][q]; }
    int** f3() { return ce; }
private:
    int** f1();//数组的创建
};
int** Matrix::f1() {

    int** p = new int* [be];
    for (int i = 0; i < be; ++i)
    {
        p[i] = new int[ae];
    }
    p[be - 1][ae - 1] = 3;
    for (int i = 0;i < ae;i++) {
        for (int j = 0;j < be;j++) {
            cin >> p[j][i];
        }
    }

    return p;

    for (int i = 0; i < ae; ++i)
    {
        delete[] p[i];
    }
    delete[] p;
}
int** operator+=(Matrix aq, Matrix bq) {

    int** p = new int* [aq.be];
    for (int i = 0; i < aq.be; ++i)
    {
        p[i] = new int[aq.ae];
    }
    if ((aq.ae != bq.ae) || (aq.be != bq.be)) {
        cout << "ERROR!";
        p = { 0 };
        return p;
    }

    for (int i = 0;i < aq.ae;i++) {
        for (int j = 0;j < aq.be;j++) {
            p[j][i] = aq.ce[j][i] + bq.ce[j][i];
        }
    }
    return p;
}
int** operator*=(Matrix aq, Matrix bq) {

    int** p = new int* [aq.be];
    for (int i = 0; i < aq.be; ++i)
    {
        p[i] = new int[aq.be];
    }
    if ((aq.ae != bq.be) || (aq.be != bq.ae)) {
        cout << "ERROR!";
        p = { 0 };
        return p;
    }

    for (int i = 0;i < aq.be;i++) {
        for (int j = 0;j < aq.be;j++) {
            int xxx = 0;
            for (int k = 0;k < aq.ae;k++) {
                xxx += aq.ce[i][k] * bq.ce[k][j];
            }
            p[j][i] = xxx;
        }
    }
    return p;
}
void Qinlang(int** p, int a, int b) {
    for (int i = 0;i < a;i++) {
        cout << endl;
        for (int j = 0;j < b;j++) {
            cout << p[j][i] << " ";
        }
    }
}
int main() {
    int ar, br, aw, bw;
    cin >> ar >> br;
    Matrix ay(ar, br);
    cin >> aw >> bw;
    Matrix by(aw, bw);
    cout << ay.f3()[br - 1][ar - 1] << endl;
    cout << endl;
    if ((ar != aw) || (br != bw)) {
        cout << "ERROR!";
    }
    else {
        Qinlang(ay *= by, ar, ar);
    }
    cout << endl<<endl;
    if ((ar != bw) || (aw != br)) {
        cout << "ERROR!";
    }
    else {
        Qinlang(ay += by, ar, ar);
    }
    cout << endl;
    ay = by;
    Qinlang(ay.f3(), aw, bw);
}