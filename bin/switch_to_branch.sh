for repo_dir in ${REPO_DIR}/*
do
  pushd "${repo_dir}" || exit 1
  git checkout main
  popd || exit 1
done