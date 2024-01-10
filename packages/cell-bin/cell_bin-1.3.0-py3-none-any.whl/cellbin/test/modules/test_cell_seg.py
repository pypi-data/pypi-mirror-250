import sys

import tifffile
import argparse

from cellbin.modules.cell_segmentation import CellSegmentation

def main():
    # parser = argparse.ArgumentParser(description="you should add those parameter")
    # parser.add_argument('-i', "--input", help="the input img path")
    # parser.add_argument('-o', "--output", help="the output file")
    # parser.add_argument("-g", "--gpu", help="the gpu index", default=-1)
    # parser.add_argument("-th", "--num_threads", help="num_threads", default="0")
    #
    # args = parser.parse_args()
    # input_path = args.input
    # output_path = args.output
    # gpu = args.gpu
    # num_threads = args.num_threads

    # if input_path is None or output_path is None:
    #     print("please check your parameters")
    #     sys.exit()
    # print(args)
    model_path = r"D:\Data\qc\new_qc_test_data\clarity\bad\test_imgs\test_download\cellseg_bcdu_SHDI_221008_tf.onnx"
    input_path = r"D:\Data\qc\new_qc_test_data\clarity\bad\B01604D4_20230324_212735_0.1_regist.tif"
    out_path = r"D:\Data\qc\new_qc_test_data\clarity\bad\tissue_cut\B01604D4_20230324_212735_0.1_regist_cell_cut.tif"
    gpu = 0
    num_threads = 0
    cell_bcdu = CellSegmentation(
        model_path=model_path,
        gpu=gpu,
        num_threads=num_threads
    )
    img = tifffile.imread(input_path)
    # 返回的mask
    mask = cell_bcdu.run(img)
    # 返回的统计数据,box_h,box_w,area
    trace = CellSegmentation.get_trace(mask)
    tifffile.imwrite(out_path, mask)


if __name__ == '__main__':
    import sys

    main()
    sys.exit()
