#include <iostream>
#include <vector>
#include <string>

using namespace std;

// Khai báo lớp SinhVien
class SinhVien {
private:
    string ten;
    int tuoi;
    string email;
    string trinhDoTiengAnh;
    bool daDongHocPhi;

public:
    // Constructor
    SinhVien(string ten, int tuoi, string email, string trinhDoTiengAnh, bool daDongHocPhi) {
        this->ten = ten;
        this->tuoi = tuoi;
        this->email = email;
        this->trinhDoTiengAnh = trinhDoTiengAnh;
        this->daDongHocPhi = daDongHocPhi;
    }

    // Getter methods
    string getTen() {
        return ten;
    }

    int getTuoi() {
        return tuoi;
    }

    string getEmail() {
        return email;
    }

    string getTrinhDoTiengAnh() {
        return trinhDoTiengAnh;
    }

    bool getDaDongHocPhi() {
        return daDongHocPhi;
    }

    // Setter methods
    void setTen(string ten) {
        this->ten = ten;
    }

    void setTuoi(int tuoi) {
        this->tuoi = tuoi;
    }

    void setEmail(string email) {
        this->email = email;
    }

    void setTrinhDoTiengAnh(string trinhDoTiengAnh) {
        this->trinhDoTiengAnh = trinhDoTiengAnh;
    }

    void setDaDongHocPhi(bool daDongHocPhi) {
        this->daDongHocPhi = daDongHocPhi;
    }

    // Method to display student information
    void hienThiThongTin() {
        cout << "Tên: " << ten << endl;
        cout << "Tuổi: " << tuoi << endl;
        cout << "Email: " << email << endl;
        cout << "Trình độ Tiếng Anh: " << trinhDoTiengAnh << endl;
        cout << "Tình trạng thanh toán học phí: " << (daDongHocPhi ? "Đã đóng" : "Chưa đóng") << endl;
    }
};

// Khai báo lớp KhoaHocTiengAnh
class KhoaHocTiengAnh {
private:
    string ten;
    string ngayBatDau;
    string ngayKetThuc;
    int soLuongSinhVienToiDa;
    vector<SinhVien*> danhSachSinhVien;

public:
    // Constructor
    KhoaHocTiengAnh(string ten, string ngayBatDau, string ngayKetThuc, int soLuongSinhVienToiDa) {
        this->ten = ten;
        this->ngayBatDau = ngayBatDau;
        this->ngayKetThuc = ngayKetThuc;
        this->soLuongSinhVienToiDa = soLuongSinhVienToiDa;
    }

    // Getter methods
    string getTen(){
    return ten;
}
string getNgayBatDau() {
    return ngayBatDau;
}

string getNgayKetThuc() {
    return ngayKetThuc;
}

int getSoLuongSinhVienToiDa() {
    return soLuongSinhVienToiDa;
}

vector<SinhVien*> getDanhSachSinhVien() {
    return danhSachSinhVien;
}

// Setter methods
void setTen(string ten) {
    this->ten = ten;
}

void setNgayBatDau(string ngayBatDau) {
    this->ngayBatDau = ngayBatDau;
}

void setNgayKetThuc(string ngayKetThuc) {
    this->ngayKetThuc = ngayKetThuc;
}

void setSoLuongSinhVienToiDa(int soLuongSinhVienToiDa) {
    this->soLuongSinhVienToiDa = soLuongSinhVienToiDa;
}

// Method to add a student to the course
void themSinhVien(SinhVien* sv) {
    if (danhSachSinhVien.size() < soLuongSinhVienToiDa) {
        danhSachSinhVien.push_back(sv);
        cout << "Thêm sinh viên " << sv->getTen() << " thành công!" << endl;
    } else {
        cout << "Không thể thêm sinh viên " << sv->getTen() << ". Số lượng sinh viên đã đủ!" << endl;
    }
}

// Method to display course information
void hienThiThongTin() {
    cout << "Tên khóa học: " << ten << endl;
    cout << "Ngày bắt đầu: " << ngayBatDau << endl;
    cout << "Ngày kết thúc: " << ngayKetThuc << endl;
    cout << "Số lượng sinh viên tối đa: " << soLuongSinhVienToiDa << endl;
    cout << "Danh sách sinh viên đăng ký: " << endl;
    for (int i = 0; i < danhSachSinhVien.size(); i++) {
        cout << "Sinh viên thứ " << i + 1 << ": " << danhSachSinhVien[i]->getTen() << endl;
    }
}
};

// Hàm main
int main() {
// Tạo đối tượng khóa học Tiếng Anh
KhoaHocTiengAnh* kh = new KhoaHocTiengAnh("Khóa học Tiếng Anh giao tiếp cơ bản", "01/06/2023", "31/08/2023", 20);
// Tạo danh sách sinh viên đăng ký khóa học
SinhVien* sv1 = new SinhVien("Nguyễn Văn A", 20, "nva@gmail.com", "Trung cấp", false);
SinhVien* sv2 = new SinhVien("Nguyễn Thị B", 21, "ntb@gmail.com", "Đại học", true);
SinhVien* sv3 = new SinhVien("Trần Văn C", 19,  "tvcb@gmail.com", "Cao đẳng", false);
SinhVien* sv4 = new SinhVien("Lê Thị D", 22, "ltd@gmail.com", "Cao đẳng", true);
SinhVien* sv5 = new SinhVien("Phạm Văn E", 20, "pve@gmail.com", "Trung cấp", true);

// Thêm sinh viên vào khóa học
kh->themSinhVien(sv1);
kh->themSinhVien(sv2);
kh->themSinhVien(sv3);
kh->themSinhVien(sv4);
kh->themSinhVien(sv5);

// Hiển thị thông tin khóa học
kh->hienThiThongTin();

return 0;