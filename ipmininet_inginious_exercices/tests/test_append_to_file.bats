setup() {
    load '../bats/test_helper/bats-support/load'
    load '../bats/test_helper/bats-assert/load'
    touch ./file
    echo "KVM (for Kernel-based Virtual Machine) is a full virtualization solution for Linux on x86
          hardware containing virtualization extensions (Intel VT or AMD-V). It consists of a 
          loadable kernel module, kvm.ko, that provides the core virtualization infrastructure and 
          a processor specific module, kvm-intel.ko or kvm-amd.ko. Using KVM, one can run multiple virtual
          machines running unmodified Linux or Windows images. Each virtual machine has private virtualized
          hardware: a network card, disk, graphics adapter, etc.
          KVM is open source software. The kernel component of KVM is included in mainline Linux, as of
          2.6.20. The userspace component of KVM is included in mainline QEMU, as of 1.3.
          Blogs from people active in KVM-related virtualization development are syndicated at http:
          planet.virt- tools.org/" > ./file
    export TEXT="ADD_TEXT_AT_END_OF_A_FILE"
    echo $TEXT >> ./file
}

@test "run append_to_file test" {
    run exercices/verif_append_to_file.sh "./file" "$TEXT"
    assert_output 'Success'
    rm ./file
}
