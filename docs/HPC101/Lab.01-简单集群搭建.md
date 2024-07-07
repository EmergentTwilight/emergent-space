---
created: 2024-07-03T10:51:33
updated: 2024-07-06T02:00:53
---
# Note

> [!NOTE] 如何写好一份实验报告
> 1. 包含以下基本内容：
>     - 实验环境：软硬件的细微差别也有可能导致实验过程和结果产生较大差异，因此记录实验环境是非常重要的。这包括宿主机硬件情况，操作系统版本，所使用的 Hypervisor 种类，虚拟机的硬件配置以及网络配置。
>     - 实验过程：实验手册已经给出了详细步骤，因此这一部分你不需要再赘述，只需要给出关键截图证明你按步骤完成了即可。我们希望看到的是你在实验过程中遇到了哪些问题，以及你是如何解决的。
>     - 实验结果及分析：对于希望你照做的实验（比如本次实验），本就有一个标准的结果，不需要进行分析。但如果是需要你自己设计的实验，那么你需要对实验结果进行分析，解释为什么会得到这样的结果。
> 2. 详略得当。一般来说，下面这两种实验报告都不是好的实验报告：
>     - 长达数十页的报告：贴满截图和源代码，正文内容却很少。
>     - 简陋的实验报告：只有几张截图，没有有效的解释。

## To learn

- [ ] `scp` 命令的使用

## 链接

实际的工程开发中，采用的一定是多文件编程: 编译器将每个代码文件分别编译后，还需要将它们合在一起变成一个软件，**合在一起的过程就是链接的过程**。这些内容在 C 语言课程中应该会覆盖到，但如果你没有学过，也不用担心，可以学习一下翁恺老师的 [智云课堂](http://classroom-zju-edu-cn-s.webvpn.zju.edu.cn:8001/livingroom?course_id=53613&sub_id=1028201&tenant_code=112) 或者 [MOOC](http://www-icourse163-org-s.webvpn.zju.edu.cn:8001/course/ZJU-200001) (第五周) 中对大程序结构的详细介绍。

链接分为静态链接和动态链接。静态链接是指在编译时将库文件的代码和程序代码合并在一起，生成一个完全独立的可执行文件。动态链接是指在程序运行时，加载库文件，从而节省存储空间，提高程序的复用性和灵活性。

- 静态链接
    - 如果你的程序与静态库链接，那么链接器会将静态库中的代码复制到你的程序中。这样，你的程序就不再依赖静态库了，可以在任何地方运行。但是，如果静态库中的代码发生了变化，你的程序并不会自动更新，你需要重新编译你的程序。
    - 在 Linux 系统上，静态库的文件名以 `.a` 结尾，比如 `libm.a`。在 Window 上，静态库的文件名以 `.lib` 结尾，比如 `libm.lib`。静态库可以使用 `ar` （archive program）工具创建。
- 动态链接
    - 当你的程序与动态库链接时，程序中创建了一个表。在程序运行前，操作系统将需要的外部函数的机器码加载到内存中，这就是动态链接过程。
    - 与静态链接相比，动态链接使程序文件更小，因为一个动态库可以被多个程序共享，节省磁盘空间。部分操作系统还允许动态库代码在内存中的共享，还能够节省内存。动态库升级时，也不需要重写编译你的程序。
    - 在 Linux 系统上，动态库的文件名以 `.so` 结尾，比如 `libm.so`。在 Window 上，动态库的文件名以 `.dll` 结尾，比如 `libm.dll`。

动态链接具有上面描述的优点，因此一般程序会尽可能地执行动态链接。

# 任务一

## 构建并安装 OpenMPI

```bash
wget https://download.open-mpi.org/release/open-mpi/v5.0/openmpi-5.0.3.tar.gz
tar -xzf openmpi-5.0.3.tar.gz
```

`README.md` 中给出的在线文档地址为 [4.1. Quick start: Installing Open MPI — Open MPI 5.0.x documentation (open-mpi.org)](https://docs.open-mpi.org/en/v5.0.x/installing-open-mpi/quickstart.html)

```bash
./configure --prefix=/usr/local/openmpi
```

```txt
Open MPI configuration:
-----------------------
Version: 5.0.3
MPI Standard Version: 3.1
Build MPI C bindings: yes
Build MPI Fortran bindings: mpif.h, use mpi, use mpi_f08
Build MPI Java bindings (experimental): no
Build Open SHMEM support: false (no spml)
Debug build: no
Platform file: (none)
 
Miscellaneous
-----------------------
Atomics: GCC built-in style atomics
Fault Tolerance support: mpi
HTML docs and man pages: installing packaged docs
hwloc: internal
libevent: internal
Open UCC: no
pmix: internal
PRRTE: internal
Threading Package: pthreads
 
Transports
-----------------------
Cisco usNIC: no
Cray uGNI (Gemini/Aries): no
Intel Omnipath (PSM2): no (not found)
Open UCX: no
OpenFabrics OFI Libfabric: no (not found)
Portals4: no (not found)
Shared memory/copy in+copy out: yes
Shared memory/Linux CMA: yes
Shared memory/Linux KNEM: no
Shared memory/XPMEM: no
TCP: yes
 
Accelerators
-----------------------
CUDA support: no
ROCm support: no
 
OMPIO File Systems
-----------------------
DDN Infinite Memory Engine: no
Generic Unix FS: yes
IBM Spectrum Scale/GPFS: no (not found)
Lustre: no (not found)
PVFS2/OrangeFS: no
```

```bash
make
```

```txt
make[3]: Entering directory '/home/usr_vm1/openmpi-5.0.3/3rd-party/libevent-2.1.12-stable'
  CC       sample/dns-example.o
  CC       buffer.lo
  CC       bufferevent.lo
  CC       bufferevent_filter.lo
  CC       bufferevent_pair.lo
  CC       bufferevent_ratelim.lo
  CC       bufferevent_sock.lo
  CC       event.lo
event.c: In function ‘event_signal_closure’:
event.c:1362:32: warning: storing the address of local variable ‘ncalls’ in ‘*ev.ev_.ev_signal.ev_pncalls’ [-Wdangling-pointer=]
 1362 |                 ev->ev_pncalls = &ncalls;
      |                 ~~~~~~~~~~~~~~~^~~~~~~~~
event.c:1356:15: note: ‘ncalls’ declared here
 1356 |         short ncalls;
      |               ^~~~~~
event.c:1356:15: note: ‘ev’ declared here
  CC       evmap.lo
  CC       evthread.lo
  CC       evutil.lo
evutil.c:213:21: warning: argument 4 of type ‘int[2]’ with mismatched bound [-Warray-parameter=]
  213 |     evutil_socket_t fd[2])
In file included from evutil.c:85:
./include/event2/util.h:310:25: note: previously declared as ‘int[]’
  310 | #define evutil_socket_t int
util-internal.h:306:47: note: in expansion of macro ‘evutil_socket_t’
  306 | int evutil_ersatz_socketpair_(int, int , int, evutil_socket_t[]);
      |                                               ^~~~~~~~~~~~~~~
```

```txt
make[2]: Entering directory '/home/usr_vm1/openmpi-5.0.3/ompi/mca/coll/libnbc'
  CC       coll_libnbc_component.lo
  CC       nbc.lo
  CC       libdict/dict.lo
  CC       libdict/hb_tree.lo
  CC       nbc_iallgather.lo
  CC       nbc_iallgatherv.lo
  CC       nbc_iallreduce.lo
  CC       nbc_ialltoall.lo
  CC       nbc_ialltoallv.lo
  CC       nbc_ialltoallw.lo
  CC       nbc_ibarrier.lo
  CC       nbc_ibcast.lo
  CC       nbc_iexscan.lo
  CC       nbc_igather.lo
  CC       nbc_igatherv.lo
  CC       nbc_ineighbor_allgather.lo
  CC       nbc_ineighbor_allgatherv.lo
  CC       nbc_ineighbor_alltoall.lo
  CC       nbc_ineighbor_alltoallv.lo
  CC       nbc_ineighbor_alltoallw.lo
  CC       nbc_ireduce.lo
  CC       nbc_ireduce_scatter.lo
  CC       nbc_ireduce_scatter_block.lo
  CC       nbc_iscan.lo
  CC       nbc_iscatter.lo
  CC       nbc_iscatterv.lo
  CC       nbc_neighbor_helpers.lo
nbc_neighbor_helpers.c: In function ‘NBC_Comm_neighbors’:
nbc_neighbor_helpers.c:98:5: warning: ‘mca_topo_base_dist_graph_neighbors’ accessing 4 bytes in a region of size 0 [-Wstringop-overflow=]
   98 |     mca_topo_base_dist_graph_neighbors (comm, indeg, sources[0], MPI_UNWEIGHTED, outdeg, destinations[0],
      |     ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   99 |                                          MPI_UNWEIGHTED);
      |                                          ~~~~~~~~~~~~~~~
nbc_neighbor_helpers.c:98:5: note: referencing argument 4 of type ‘int[0]’
nbc_neighbor_helpers.c:98:5: note: referencing argument 6 of type ‘int[0]’
nbc_neighbor_helpers.c:98:5: warning: ‘mca_topo_base_dist_graph_neighbors’ accessing 4 bytes in a region of size 0 [-Wstringop-overflow=]
nbc_neighbor_helpers.c:98:5: note: referencing argument 7 of type ‘int[0]’
In file included from nbc_neighbor_helpers.c:16:
../../../../ompi/mca/topo/base/base.h:198:1: note: in a call to function ‘mca_topo_base_dist_graph_neighbors’
  198 | mca_topo_base_dist_graph_neighbors(ompi_communicator_t *comm,
      | ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
nbc_neighbor_helpers.c:98:5: warning: ‘mca_topo_base_dist_graph_neighbors’ accessing 4 bytes in a region of size 0 [-Wstringop-overflow=]
   98 |     mca_topo_base_dist_graph_neighbors (comm, indeg, sources[0], MPI_UNWEIGHTED, outdeg, destinations[0],
      |     ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   99 |                                          MPI_UNWEIGHTED);
      |                                          ~~~~~~~~~~~~~~~
nbc_neighbor_helpers.c:98:5: note: referencing argument 4 of type ‘int[0]’
nbc_neighbor_helpers.c:98:5: note: referencing argument 6 of type ‘int[0]’
nbc_neighbor_helpers.c:98:5: warning: ‘mca_topo_base_dist_graph_neighbors’ accessing 4 bytes in a region of size 0 [-Wstringop-overflow=]
nbc_neighbor_helpers.c:98:5: note: referencing argument 7 of type ‘int[0]’
../../../../ompi/mca/topo/base/base.h:198:1: note: in a call to function ‘mca_topo_base_dist_graph_neighbors’
  198 | mca_topo_base_dist_graph_neighbors(ompi_communicator_t *comm,
      | ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
nbc_neighbor_helpers.c:98:5: warning: ‘mca_topo_base_dist_graph_neighbors’ accessing 4 bytes in a region of size 0 [-Wstringop-overflow=]
   98 |     mca_topo_base_dist_graph_neighbors (comm, indeg, sources[0], MPI_UNWEIGHTED, outdeg, destinations[0],
      |     ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   99 |                                          MPI_UNWEIGHTED);
      |                                          ~~~~~~~~~~~~~~~
nbc_neighbor_helpers.c:98:5: note: referencing argument 4 of type ‘int[0]’
nbc_neighbor_helpers.c:98:5: note: referencing argument 6 of type ‘int[0]’
nbc_neighbor_helpers.c:98:5: warning: ‘mca_topo_base_dist_graph_neighbors’ accessing 4 bytes in a region of size 0 [-Wstringop-overflow=]
nbc_neighbor_helpers.c:98:5: note: referencing argument 7 of type ‘int[0]’
../../../../ompi/mca/topo/base/base.h:198:1: note: in a call to function ‘mca_topo_base_dist_graph_neighbors’
  198 | mca_topo_base_dist_graph_neighbors(ompi_communicator_t *comm,
      | ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  CCLD     libmca_coll_libnbc.la
ar: `u' modifier ignored since `D' is the default (see `U')
```

```bash
ompi_info
```

```txt
Package: Open MPI usr_vm1@vm1 Distribution
                Open MPI: 5.0.3
  Open MPI repo revision: v5.0.3
   Open MPI release date: Apr 08, 2024
                 MPI API: 3.1.0
            Ident string: 5.0.3
                  Prefix: /usr/local/openmpi
 Configured architecture: x86_64-pc-linux-gnu
           Configured by: usr_vm1
           Configured on: Fri May 31 18:01:20 UTC 2024
          Configure host: vm1
  Configure command line: '--prefix=/usr/local/openmpi'
                Built by: usr_vm1
                Built on: Friday, May 31, 2024 PM06:08:42 UTC
              Built host: vm1
              C bindings: yes
             Fort mpif.h: no
            Fort use mpi: no
       Fort use mpi size: deprecated-ompi-info-value
        Fort use mpi_f08: no
 Fort mpi_f08 compliance: The mpi_f08 module was not built
  Fort mpi_f08 subarrays: no
           Java bindings: no
  Wrapper compiler rpath: runpath
              C compiler: gcc
     C compiler absolute: /bin/gcc
  C compiler family name: GNU
      C compiler version: 12.2.0
            C++ compiler: g++
   C++ compiler absolute: /bin/g++
           Fort compiler: none
       Fort compiler abs: none
         Fort ignore TKR: no
   Fort 08 assumed shape: no
      Fort optional args: no
          Fort INTERFACE: no
    Fort ISO_FORTRAN_ENV: no
       Fort STORAGE_SIZE: no
      Fort BIND(C) (all): no
      Fort ISO_C_BINDING: no
 Fort SUBROUTINE BIND(C): no
       Fort TYPE,BIND(C): no
 Fort T,BIND(C,name="a"): no
            Fort PRIVATE: no
           Fort ABSTRACT: no
       Fort ASYNCHRONOUS: no
          Fort PROCEDURE: no
         Fort USE...ONLY: no
           Fort C_FUNLOC: no
 Fort f08 using wrappers: no
         Fort MPI_SIZEOF: no
             C profiling: yes
   Fort mpif.h profiling: no
  Fort use mpi profiling: no
   Fort use mpi_f08 prof: no
          Thread support: posix (MPI_THREAD_MULTIPLE: yes, OPAL support: yes,
                          OMPI progress: no, Event lib: yes)
           Sparse Groups: no
  Internal debug support: no
  MPI interface warnings: yes
     MPI parameter check: runtime
Memory profiling support: no
Memory debugging support: no
              dl support: yes
   Heterogeneous support: no
       MPI_WTIME support: native
     Symbol vis. support: yes
   Host topology support: yes
            IPv6 support: no
          MPI extensions: affinity, cuda, ftmpi, rocm, shortfloat
 Fault Tolerance support: yes
          FT MPI support: yes
  MPI_MAX_PROCESSOR_NAME: 256
    MPI_MAX_ERROR_STRING: 256
     MPI_MAX_OBJECT_NAME: 64
        MPI_MAX_INFO_KEY: 36
        MPI_MAX_INFO_VAL: 256
       MPI_MAX_PORT_NAME: 1024
  MPI_MAX_DATAREP_STRING: 128
         MCA accelerator: null (MCA v2.1.0, API v1.0.0, Component v5.0.3)
           MCA allocator: basic (MCA v2.1.0, API v2.0.0, Component v5.0.3)
           MCA allocator: bucket (MCA v2.1.0, API v2.0.0, Component v5.0.3)
           MCA backtrace: execinfo (MCA v2.1.0, API v2.0.0, Component v5.0.3)
                 MCA btl: self (MCA v2.1.0, API v3.3.0, Component v5.0.3)
                 MCA btl: sm (MCA v2.1.0, API v3.3.0, Component v5.0.3)
                 MCA btl: tcp (MCA v2.1.0, API v3.3.0, Component v5.0.3)
                  MCA dl: dlopen (MCA v2.1.0, API v1.0.0, Component v5.0.3)
                  MCA if: linux_ipv6 (MCA v2.1.0, API v2.0.0, Component
                          v5.0.3)
                  MCA if: posix_ipv4 (MCA v2.1.0, API v2.0.0, Component
                          v5.0.3)
         MCA installdirs: env (MCA v2.1.0, API v2.0.0, Component v5.0.3)
         MCA installdirs: config (MCA v2.1.0, API v2.0.0, Component v5.0.3)
              MCA memory: patcher (MCA v2.1.0, API v2.0.0, Component v5.0.3)
               MCA mpool: hugepage (MCA v2.1.0, API v3.1.0, Component v5.0.3)
             MCA patcher: overwrite (MCA v2.1.0, API v1.0.0, Component
                          v5.0.3)
              MCA rcache: grdma (MCA v2.1.0, API v3.3.0, Component v5.0.3)
           MCA reachable: weighted (MCA v2.1.0, API v2.0.0, Component v5.0.3)
               MCA shmem: mmap (MCA v2.1.0, API v2.0.0, Component v5.0.3)
               MCA shmem: posix (MCA v2.1.0, API v2.0.0, Component v5.0.3)
               MCA shmem: sysv (MCA v2.1.0, API v2.0.0, Component v5.0.3)
                MCA smsc: cma (MCA v2.1.0, API v1.0.0, Component v5.0.3)
             MCA threads: pthreads (MCA v2.1.0, API v1.0.0, Component v5.0.3)
               MCA timer: linux (MCA v2.1.0, API v2.0.0, Component v5.0.3)
                 MCA bml: r2 (MCA v2.1.0, API v2.1.0, Component v5.0.3)
                MCA coll: adapt (MCA v2.1.0, API v2.4.0, Component v5.0.3)
                MCA coll: basic (MCA v2.1.0, API v2.4.0, Component v5.0.3)
                MCA coll: han (MCA v2.1.0, API v2.4.0, Component v5.0.3)
                MCA coll: inter (MCA v2.1.0, API v2.4.0, Component v5.0.3)
                MCA coll: libnbc (MCA v2.1.0, API v2.4.0, Component v5.0.3)
                MCA coll: self (MCA v2.1.0, API v2.4.0, Component v5.0.3)
                MCA coll: sync (MCA v2.1.0, API v2.4.0, Component v5.0.3)
                MCA coll: tuned (MCA v2.1.0, API v2.4.0, Component v5.0.3)
                MCA coll: ftagree (MCA v2.1.0, API v2.4.0, Component v5.0.3)
                MCA coll: monitoring (MCA v2.1.0, API v2.4.0, Component
                          v5.0.3)
                MCA coll: sm (MCA v2.1.0, API v2.4.0, Component v5.0.3)
                MCA fbtl: posix (MCA v2.1.0, API v2.0.0, Component v5.0.3)
               MCA fcoll: dynamic (MCA v2.1.0, API v2.0.0, Component v5.0.3)
               MCA fcoll: dynamic_gen2 (MCA v2.1.0, API v2.0.0, Component
                          v5.0.3)
               MCA fcoll: individual (MCA v2.1.0, API v2.0.0, Component
                          v5.0.3)
               MCA fcoll: vulcan (MCA v2.1.0, API v2.0.0, Component v5.0.3)
                  MCA fs: ufs (MCA v2.1.0, API v2.0.0, Component v5.0.3)
                MCA hook: comm_method (MCA v2.1.0, API v1.0.0, Component
                          v5.0.3)
                  MCA io: ompio (MCA v2.1.0, API v2.0.0, Component v5.0.3)
                  MCA io: romio341 (MCA v2.1.0, API v2.0.0, Component v5.0.3)
                  MCA op: avx (MCA v2.1.0, API v1.0.0, Component v5.0.3)
                 MCA osc: sm (MCA v2.1.0, API v3.0.0, Component v5.0.3)
                 MCA osc: monitoring (MCA v2.1.0, API v3.0.0, Component
                          v5.0.3)
                 MCA osc: rdma (MCA v2.1.0, API v3.0.0, Component v5.0.3)
                MCA part: persist (MCA v2.1.0, API v4.0.0, Component v5.0.3)
                 MCA pml: cm (MCA v2.1.0, API v2.1.0, Component v5.0.3)
                 MCA pml: monitoring (MCA v2.1.0, API v2.1.0, Component
                          v5.0.3)
                 MCA pml: ob1 (MCA v2.1.0, API v2.1.0, Component v5.0.3)
                 MCA pml: v (MCA v2.1.0, API v2.1.0, Component v5.0.3)
            MCA sharedfp: individual (MCA v2.1.0, API v2.0.0, Component
                          v5.0.3)
            MCA sharedfp: lockedfile (MCA v2.1.0, API v2.0.0, Component
                          v5.0.3)
            MCA sharedfp: sm (MCA v2.1.0, API v2.0.0, Component v5.0.3)
                MCA topo: basic (MCA v2.1.0, API v2.2.0, Component v5.0.3)
                MCA topo: treematch (MCA v2.1.0, API v2.2.0, Component
                          v5.0.3)
           MCA vprotocol: pessimist (MCA v2.1.0, API v2.0.0, Component
                          v5.0.3)
```

## 构建 BLAS

```bash
wget https://www.netlib.org/blas/blas-3.12.0.tgz
tar -xzf blas-3.12.0.tgz
```

# 任务零

[VMware Workstation安装 Debian12 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/645064573)

## 配置 ssh

### 添加 sudoer

以 `root` 用户登录：

```bash
visudo
```

找到并修改：

```txt
root    ALL=(ALL:ALL) ALL
username    ALL=(ALL:ALL) ALL  # 添加这一行内容
```

### 进行 ssh 配置

回到 `username` 用户：

```bash
sudo apt upgrade  # 更新包列表
sudo apt install openssh-server  # 安装 OpenSSH 服务器
sudo systemctl start ssh  # 启动 SSH 服务
sudo systemctl enable ssh  # 设置 SSH 服务开机自启动
sudo systemctl status ssh  # 验证 SSH 服务是否正在运行

ip addr  # 获取 IP 地址
```






# Docker 复现实验

## 集群搭建

### Docker 容器创建

首先安装好 Docker Desktop，并打开，pull debian image，创建容器 `hpl-setup` 并挂载主机的一个文件共享目录，方便文件传输：

```bash
docker run -v D:\HPC\docker_share:/home/share -it --name hpl-setup debian:latest
```

### 容器内环境配置

首先进行基本的配置：

```bash
apt update
apt install build-essential
apt install wget
apt install gfortran
apt install openssh-server
apt install python3 python3-pip
apt install iputils-ping
apt install procps

systemctl enable ssh  # 设置 ssh 服务自启动
passwd root  # 设置新的密码
echo "PermitRootLogin yes" >> /etc/ssh/sshd_config  # 允许使用 ssh 登录 root 用户
```

安装 OpenMPI：

```bash
wget "https://download.open-mpi.org/release/open-mpi/v5.0/openmpi-5.0.3.tar.gz"
tar xvf openmpi-5.0.3.tar.gz
cd openmpi-5.0.3
./configure
make
make install # 安装到系统目录 /usr/local 需要 root 权限
ldconfig # 更新动态链接库缓存
ompi_info --all # 查看安装信息
```

下载编译 BLAS：

```bash
wget "http://www.netlib.org/blas/blas-3.12.0.tgz"
tar xvf blas-3.12.0.tgz
cd BLAS-3.12.0
make
```

下载编译 HPL：

```bash
wget "https://netlib.org/benchmark/hpl/hpl-2.3.tar.gz"
tar xvf hpl-2.3.tar.gz
cd hpl-2.3
cp setup/Make.Linux_PII_FBLAS .
vim Make.Linux_PII_FBLAS # 修改 Makefile
make arch=Linux_PII_FBLAS
```

`Make.Linux_PII_FBLAS` 中做的修改如下：

```

TOPdir = $(HOME)/hpl-2.3        | TOPdir = $(HOME)/hpl
MPdir  = /usr/local             | MPdir  = /usr/local/mpi
MPlib  = $(MPdir)/lib/libmpi.so | MPlib  = $(MPdir)/lib/libmpich.a
LAdir  = $(HOME)/BLAS-3.12.0    | LAdir  = $(HOME)/netlib/ARCHIVES/Linux_PII
LAlib  = $(LAdir)/blas_LINUX.a  | LAlib  = $(LAdir)/libf 77 blas.a $(LAdir)/libatlas.a
LINKER = /usr/bin/gfortran      | LINKER = /usr/bin/g 77
```

### 集群创建和网络配置

将 `hpl-setup` 保存为新的镜像：

```bash
docker commit hpl-setup hpl-mpi-configured
```

用新的镜像创建多个容器实例：

```bash
docker run -v D:\HPC\docker_share:/home/share -it --name node01 hpl-mpi-configured
docker run -v D:\HPC\docker_share:/home/share -it --name node02 hpl-mpi-configured
docker run -v D:\HPC\docker_share:/home/share -it --name node03 hpl-mpi-configured
docker run -v D:\HPC\docker_share:/home/share -it --name node04 hpl-mpi-configured
```

获取所有容器的 ip 地址并在 `node01` 中修改 `hosts` 文件：

```txt
127.0.0.1       localhost
172.17.0.3      node02
172.17.0.4      node03
172.17.0.5      node04
```

配置 ssh：

```bash
ssh-keygen
ssh-copy-id root@node02
ssh-copy-id root@node03
ssh-copy-id root@node04
```

验证无密码登录成功。

### 集群性能配置

```bash
docker update --cpuset-cpus="0-2" node01
docker update --cpuset-cpus="3-5" node02
docker update --cpuset-cpus="6-8" node03
docker update --cpuset-cpus="9-11" node04
```

配置 hostfile：

```txt
localhost
node02
node03
node04
```

```bash
mpirun --allow-run-as-root --hostfile hf ./xhpl
```

### **运行结果**

```txt
\HPLinpack benchmark input file
Innovative Computing Laboratory, University of Tennessee
HPL.out      output file name (if any)
6            device out (6=stdout,7=stderr,file)
1            # of problems sizes (N)
20000         Ns
1            # of NBs
64           NBs
0            PMAP process mapping (0=Row-,1=Column-major)
1            # of process grids (P x Q)
3            Ps
4            Qs
16.0         threshold
1            # of panel fact
2            PFACTs (0=left, 1=Crout, 2=Right)
1            # of recursive stopping criterium
4            NBMINs (>= 1)
1            # of panels in recursion
2            NDIVs
1            # of recursive panel fact.
1            RFACTs (0=left, 1=Crout, 2=Right)
1            # of broadcast
1            BCASTs (0=1rg,1=1rM,2=2rg,3=2rM,4=Lng,5=LnM)
1            # of lookahead depth
1            DEPTHs (>=0)
2            SWAP (0=bin-exch,1=long,2=mix)
64           swapping threshold
0            L1 in (0=transposed,1=no-transposed) form
0            U  in (0=transposed,1=no-transposed) form
1            Equilibration (0=no,1=yes)
8            memory alignment in double (> 0)
```

```txt
================================================================================
HPLinpack 2.3  --  High-Performance Linpack benchmark  --   December 2, 2018
Written by A. Petitet and R. Clint Whaley,  Innovative Computing Laboratory, UTK
Modified by Piotr Luszczek, Innovative Computing Laboratory, UTK
Modified by Julien Langou, University of Colorado Denver
================================================================================

An explanation of the input/output parameters follows:
T/V    : Wall time / encoded variant.
N      : The order of the coefficient matrix A.
NB     : The partitioning blocking factor.
P      : The number of process rows.
Q      : The number of process columns.
Time   : Time in seconds to solve the linear system.
Gflops : Rate of execution for solving the linear system.

The following parameter values will be used:

N      :   20000
NB     :      64
PMAP   : Row-major process mapping
P      :       3
Q      :       4
PFACT  :   Right
NBMIN  :       4
NDIV   :       2
RFACT  :   Crout
BCAST  :  1ringM
DEPTH  :       1
SWAP   : Mix (threshold = 64)
L1     : transposed form
U      : transposed form
EQUIL  : yes
ALIGN  : 8 double precision words

--------------------------------------------------------------------------------

- The matrix A is randomly generated for each test.
- The following scaled residual check will be computed:
      ||Ax-b||_oo / ( eps * ( || x ||_oo * || A ||_oo + || b ||_oo ) * N )
- The relative machine precision (eps) is taken to be               1.110223e-16
- Computational tests pass if scaled residuals are less than                16.0

================================================================================
T/V                N    NB     P     Q               Time                 Gflops
--------------------------------------------------------------------------------
WR11C2R4       20000    64     3     4             201.83             2.6428e+01
HPL_pdgesv() start time Fri Jul  5 17:39:02 2024

HPL_pdgesv() end time   Fri Jul  5 17:42:24 2024

--------------------------------------------------------------------------------
||Ax-b||_oo/(eps*(||A||_oo*||x||_oo+||b||_oo)*N)=   3.38456923e-03 ...... PASSED
================================================================================

Finished      1 tests with the following results:
              1 tests completed and passed residual checks,
              0 tests completed and failed residual checks,
              0 tests skipped because of illegal input values.
--------------------------------------------------------------------------------

End of Tests.
================================================================================
```
