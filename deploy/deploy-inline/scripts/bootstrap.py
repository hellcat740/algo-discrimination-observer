"""Vercel 构建阶段引导：从 GitHub 拉取完整服务端代码（api/app、api/analysis）。"""
import io
import os
import tarfile
import urllib.request

REPO_TARBALL = os.environ.get(
    "BOOTSTRAP_REPO_TARBALL",
    "https://codeload.github.com/hellcat740/algo-observer-server/tar.gz/refs/heads/main",
)


def main() -> None:
    print(f"[bootstrap] fetching {REPO_TARBALL}", flush=True)
    with urllib.request.urlopen(REPO_TARBALL, timeout=180) as resp:
        data = resp.read()
    print(f"[bootstrap] downloaded {len(data)} bytes", flush=True)

    tf = tarfile.open(fileobj=io.BytesIO(data), mode="r:gz")
    extracted = 0
    for m in tf.getmembers():
        parts = m.name.split("/", 1)
        if len(parts) != 2 or not parts[1]:
            continue
        m.name = parts[1]  # 去掉仓库根目录前缀
        if not (m.name.startswith("api/") or m.name in ("requirements.txt", "vercel.json")):
            continue
        try:
            tf.extract(m, ".", filter="data")  # Python 3.12+
        except TypeError:  # 兼容旧解释器
            tf.extract(m, ".")
        extracted += 1
    print(f"[bootstrap] extracted {extracted} files", flush=True)


if __name__ == "__main__":
    main()
