setup() {
    load '../bats/test_helper/bats-support/load'
    load '../bats/test_helper/bats-assert/load'
}

@test "run create_dir test when directory exists" {
    mkdir ./dir
    run exercices/verif_create_dir.sh "./dir"
    assert_output 'Success'
    rm -r ./dir
}

@test "run create_file test when directory does not exist" {
    mkdir ./dir2
    rm -r ./dir2
    run exercices/verif_create_dir.sh "./dir2"
    assert_output 'Failed'
}
