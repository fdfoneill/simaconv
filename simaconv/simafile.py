#!/usr/bin/env python2

#######################################################
# Author: F. Dan O'Neill
# Date: 7/5/2019
########################################################

import os, sys, logging
logging.basicConfig(level=os.environ.get("LOGLEVEL","DEBUG"))
log = logging.getLogger(__name__)

import argparse, csv, json, glob

log.info("Importing arcpy")
import arcpy
arcpy.env.overwriteOutput = True


SHORTNAMES_DTYPES_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)),"resources","shortnames_and_dtypes.json")


def cleanFile(csv_path):
	"""Attempts to strip out non-utf characters and fix quotes on "lat" and "lng"""

	with open(csv_path,'r') as rf:
		data = rf.readlines()

	outData = []
	for line in data:
		line = line.replace('"lat"',"'lat'")
		line = line.replace('"lng"',"'lng'")
		line = line.replace('"type"',"'type'")
		line = line.replace('"Polygon"',"'Polygon'")
		line = line.replace('"coordinates"',"'coordinates'")
		outData.append(line)

	with open(csv_path,'w') as wf:
		wf.writelines(outData)

class SimaFile:
	"""

	***

	Attributes
	----------
	path
	data
	columns
	columns_short
	columns_type
	geom_name

	Methods
	-------
	renameColumnsShort
	writeShapefile
	"""
	def __init__(self,file_path):
		self.path = file_path
		# get list of OrderedDicts
		self.data = []
		with open(file_path) as csv_file:
			csv_reader = csv.DictReader(csv_file,delimiter=',',quotechar='"',quoting=csv.QUOTE_ALL,skipinitialspace=True)
			for row in csv_reader:
				self.data.append(row)
		# extract column names
		self.columns = list(self.data[0].keys())
		self.columns_short = {c:c for c in self.columns}
		self.columns_type = {c:None for c in self.columns}
		self.geom_name = "polyline"

	def loadJson(self,json_path=SHORTNAMES_DTYPES_FILE):
		"""Sets self.columns_short and self.columns_type to values from json"""
		with open(json_path,'r') as rf:
			jsonData = json.loads(rf.read())
		print("Columns with no matching shortName:")
		for k in self.columns_short.keys():
			if jsonData.get(k,None) is not None:
				self.columns_short[k] = jsonData[k]['short_name']
			else:
				print(k)
		print("Columns with no matching dType:")
		for k in self.columns_type.keys():
			if jsonData.get(k,None) is not None:
				self.columns_type[k] = jsonData[k]['dtype']
			else:
				print(k)
		print("Done.")

	def generatePolygon(self,latLonList):
		try:
			lll = eval(latLonList)
			innerArray = []
			log.debug("Appending points")
			for p in lll:
				innerArray.append(arcpy.Point(float(p["lng"]),float(p["lat"])))
			if len(innerArray) < 3:
				return False
			log.debug("Creating arcPy array")
			array = arcpy.Array(innerArray)
			log.debug("Creating polyline")
			polygon = arcpy.Polygon(array,arcpy.SpatialReference(4326))
			return polygon
		except Exception as e:
			log.exception("Error in generatePolygon()")

	def writeShapefile(self,out_file_path):
		cur = None
		failures = 0
		# clear mysterious '' column name
		for i in range(len(self.columns)):
			if self.columns[i] == "''":
				self.columns.pop(i)
				break
		# check that columns_type is not None
		for k in self.columns_type.keys():
			if self.columns_type[k] is None:
				print("ERROR: Set columns_type")
				return False
		# create output shapefile
		arcpy.CreateFeatureclass_management(os.path.dirname(out_file_path),
			os.path.basename(out_file_path),
			geometry_type="POLYGON",
			spatial_reference=arcpy.SpatialReference(4326)
			)
		for field in self.columns:
			field_name = self.columns_short[field]
			field_type = self.columns_type[field]
			if field == self.geom_name:
				continue
			arcpy.AddField_management(out_file_path,field_name,field_type)
		try:
			cur = arcpy.da.InsertCursor(out_file_path,["SHAPE@"]+[self.columns_short[c] for c in self.columns if c != self.geom_name])
			i = 0
			for row in self.data:
				i += 1
				print("Generating row {}".format(i))
				cursorLine = []
				geom = self.generatePolygon(row[self.geom_name])
				if not geom:
					print("Failed to generate geometry")
					failures += 1
					continue
				cursorLine.append(geom)
				for c in self.columns:
					if c == self.geom_name:
						continue
					cursorLine.append(row[c])
				cur.insertRow(cursorLine)
		except Exception as e:
			print("Failed: {}".format(e))
			return False
		finally:
			if cur:
				del cur
		print("Succeeded: {} rows failed to generate".format(failures))
		return True

def main():
	parser = argparse.ArgumentParser(description="Parses SIMA csv file and outputs polygon shapefile")
	parser.add_argument('csv_path',
		type=str,
		help='Path to csv file')
	parser.add_argument('shapefile_path',
		type=str,
		help='Path to output shapefile')
	args = parser.parse_args()
	cleanFile(args.csv_path)
	sf = SimaFile(args.csv_path)
	sf.loadJson()
	sf.writeShapefile(args.shapefile_path)

if __name__ == "__main__":
	main()
