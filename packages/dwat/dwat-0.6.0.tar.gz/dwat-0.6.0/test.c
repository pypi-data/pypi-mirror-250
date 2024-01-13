struct b {
    long a;
    int c;
    char z;
}__attribute((packed));

struct a {
    struct b a;
    struct b b;
    int d;
    unsigned long long c;
};

struct c {
    unsigned int b;
    unsigned int c;
}__attribute__((aligned(16)));

struct rb {
    unsigned char a;
    unsigned long b;
    unsigned long c;
};

struct list {
    unsigned long a;
    unsigned long b;
};

struct s1 {
    char c1;
    char c2;
    char c3;
    char c4;
    char c5;
    char c6;
    char c7;
    char c8;
    char c9;
};

struct s2 {
    char c;
    unsigned int l;
};

struct s3 {
    char c;
    unsigned long l;
};

struct vma {
    unsigned char f;
    struct s1 x;
    struct s2 y;
};

int main() {
    struct a a;
    struct vma c;
}
