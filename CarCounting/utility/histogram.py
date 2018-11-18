#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image

def make_regalur_image(img, size = (64, 64)):
	return img.resize(size).convert('RGB')

def split_image(img, part_size = (16, 16)):
	w, h = img.size
	pw, ph = part_size
	
	assert w % pw == h % ph == 0
	
	return [img.crop((i, j, i+pw, j+ph)).copy() \
				for i in range(0, w, pw) \
				for j in range(0, h, ph)]

def hist_similar(lh, rh):
	assert len(lh) == len(rh)
	return sum(1 - (0 if l == r else float(abs(l - r))/max(l, r)) for l, r in zip(lh, rh))/len(lh)

def calc_similar(li, ri):
	return sum(hist_similar(l.histogram(), r.histogram()) for l, r in zip(split_image(li), split_image(ri))) / 16.0

def calc_similar_by_path(lf, rf):
	li, ri = make_regalur_image(Image.open(lf)), make_regalur_image(Image.open(rf))
	return calc_similar(li, ri)

