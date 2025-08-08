import argparse
import os
import tempfile
import shutil

def normalize_domain(line):
    line = line.strip().lower()
    if not line or line.startswith("#"):
        return line
    parts = line.split()
    return parts[-1]  # 最后一列是域名

def remove_domains(file_to_remove, files_to_process):
    # 读取删除列表
    with open(file_to_remove, "r", encoding="utf-8") as f_remove:
        domains_to_remove = {
            normalize_domain(line)
            for line in f_remove
            if line.strip() and not line.strip().startswith("#")
        }

    for file_path in files_to_process:
        temp_fd, temp_path = tempfile.mkstemp()
        with open(file_path, "r", encoding="utf-8") as f_in, \
             open(temp_path, "w", encoding="utf-8") as f_out:
            for line in f_in:
                domain = normalize_domain(line)
                # 保留空行、注释行，或不在删除列表中的行
                if not domain or domain.startswith("#") or domain not in domains_to_remove:
                    f_out.write(line)
        os.close(temp_fd)
        shutil.move(temp_path, file_path)
        print(f"[OK] Processed: {file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove domains from multiple files.")
    parser.add_argument("-remove", required=True, help="File containing domains to be removed")
    parser.add_argument(
        "-from",
        required=True,
        dest="from_files",
        nargs="+",  # 支持多个文件
        help="One or more files to remove domains from"
    )
    args = parser.parse_args()

    remove_domains(args.remove, args.from_files)
