
#include "CloudVisualizer.h"
#include <pcl/point_cloud.h>
#include <pcl/point_types.h>
#include <pcl/io/pcd_io.h>
#include <pcl/io/ply_io.h>
#include <pcl/common/time.h>
#include <pcl/sample_consensus/model_types.h>
#include <pcl/sample_consensus/method_types.h>
#include <pcl/sample_consensus/sac_model_plane.h>
#include <pcl/segmentation/sac_segmentation.h>
#include <pcl/filters/extract_indices.h>
#include <pcl/filters/voxel_grid.h>
#include <pcl/kdtree/kdtree_flann.h>
#include <pcl/kdtree/io.h>
#include <pcl/segmentation/euclidean_cluster_comparator.h>
#include <pcl/segmentation/extract_clusters.h>
 #include <iostream>
 #include <vector>
 #include <pcl/point_types.h>
 #include <pcl/io/pcd_io.h>
#include <pcl/search/search.h>
 #include <pcl/search/kdtree.h>
 #include <pcl/features/normal_3d.h>
#include <pcl/visualization/cloud_viewer.h>
 #include <pcl/filters/filter_indices.h> // for pcl::removeNaNFromPointCloud
#include <pcl/segmentation/region_growing.h>
#include <bits/stdc++.h>
#include <algorithm>

void pointPickingCallback(const pcl::visualization::PointPickingEvent& event, void* cookie)
{
    static int pickCount = 0;
    static pcl::PointXYZRGBA lastPoint;

    pcl::PointXYZRGBA p;
    event.getPoint(p.x, p.y, p.z);

    cout << "POINT CLICKED: " << p.x << " " << p.y << " " << p.z << endl;

    // if we have picked a point previously, compute the distance
    if(pickCount % 2 == 1)
    {
        double d = std::sqrt((p.x - lastPoint.x) * (p.x - lastPoint.x) + (p.y - lastPoint.y) * (p.y - lastPoint.y) + (p.z - lastPoint.z) * (p.z - lastPoint.z));
        cout << "DISTANCE BETWEEN THE POINTS: " << d << endl;
    }

    // update the last point and pick count
    lastPoint.x = p.x;
    lastPoint.y = p.y;
    lastPoint.z = p.z;
    pickCount++;
}


void keyboardCallback(const pcl::visualization::KeyboardEvent &event, void* viewer_void)
{
    // handle key down events
    if(event.keyDown())
    {
        // handle any keys of interest
        switch(event.getKeyCode())
        {
            case 'a':
                cout << "KEYPRESS DETECTED: '" << event.getKeySym() << "'" << endl;
                break;
            default:
                break;
        }
    }
}


bool openCloud(pcl::PointCloud<pcl::PointXYZRGBA>::Ptr &cloudOut, const char* fileName)
{
    // convert the file name to string
    std::string fileNameStr(fileName);

    // handle various file types
    std::string fileExtension = fileNameStr.substr(fileNameStr.find_last_of(".") + 1);
    if(fileExtension.compare("pcd") == 0)
    {
        // attempt to open the file
        if(pcl::io::loadPCDFile<pcl::PointXYZRGBA>(fileNameStr, *cloudOut) == -1)
        {
            PCL_ERROR("error while attempting to read pcd file: %s \n", fileNameStr.c_str());
            return false;
        }
        else
        {
            return true;
        }
    }
    else if(fileExtension.compare("ply") == 0)
    {
        // attempt to open the file
        if(pcl::io::loadPLYFile<pcl::PointXYZRGBA>(fileNameStr, *cloudOut) == -1)
        {
            PCL_ERROR("error while attempting to read pcl file: %s \n", fileNameStr.c_str());
            return false;
        }
        else
        {
            return true;
        }
    }
    else
    {
        PCL_ERROR("error while attempting to read unsupported file: %s \n", fileNameStr.c_str());
        return false;
    }
}


void segmentPlane(const pcl::PointCloud<pcl::PointXYZRGBA>::ConstPtr &cloudIn, pcl::PointIndices::Ptr &inliers, double distanceThreshold, int maxIterations)
{
    // store the model coefficients
    pcl::ModelCoefficients::Ptr coefficients(new pcl::ModelCoefficients);

    // Create the segmentation object for the planar model and set the parameters
    pcl::SACSegmentation<pcl::PointXYZRGBA> seg;
    seg.setOptimizeCoefficients(true);
    seg.setModelType(pcl::SACMODEL_PLANE);
    seg.setMethodType(pcl::SAC_RANSAC);
    seg.setMaxIterations(maxIterations);
    seg.setDistanceThreshold(distanceThreshold);

    // Segment the largest planar component from the remaining cloud
    seg.setInputCloud(cloudIn);
    seg.segment(*inliers, *coefficients);
}


void removePoints(const pcl::PointCloud<pcl::PointXYZRGBA>::Ptr &cloudIn, pcl::PointCloud<pcl::PointXYZRGBA>::Ptr &cloudOut, const pcl::PointIndices::ConstPtr &inliers)
{
    pcl::ExtractIndices<pcl::PointXYZRGBA> extract;
    extract.setInputCloud(cloudIn);
    extract.setIndices (inliers);
    extract.setNegative(true);
    extract.filter(*cloudOut);
}

float distance(float x1, float y1, float x2, float y2)
{
    // Calculating distance
    return sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2) * 1.0);
}

int main(int argc, char** argv)
{
  char* filename = argv[1];
  pcl::PointCloud<pcl::PointXYZRGBA>::Ptr cloud (new pcl::PointCloud<pcl::PointXYZRGBA>);
  openCloud(cloud, filename);

  pcl::search::Search<pcl::PointXYZRGBA>::Ptr tree (new pcl::search::KdTree<pcl::PointXYZRGBA>);
  pcl::PointCloud <pcl::Normal>::Ptr normals (new pcl::PointCloud <pcl::Normal>);
  pcl::NormalEstimation<pcl::PointXYZRGBA, pcl::Normal> normal_estimator;
  normal_estimator.setSearchMethod (tree);
  normal_estimator.setInputCloud (cloud);
  normal_estimator.setKSearch (50);
  normal_estimator.compute (*normals);

  pcl::IndicesPtr indices (new std::vector <int>);
  pcl::removeNaNFromPointCloud(*cloud, *indices);

  pcl::RegionGrowing<pcl::PointXYZRGBA, pcl::Normal> reg;
  reg.setMinClusterSize (5000);
  reg.setMaxClusterSize (1000000);
  reg.setSearchMethod (tree);
  reg.setNumberOfNeighbours (30);
  reg.setInputCloud (cloud);
  reg.setIndices (indices);
  reg.setInputNormals (normals);
  reg.setSmoothnessThreshold (3.0 / 180.0 * M_PI);//3.0
  reg.setCurvatureThreshold (1.0);

  std::vector <pcl::PointIndices> clusters;
  std::vector<int> cluster_sizes;
  reg.extract (clusters);

  //std::cout << "Number of clusters is equal to " << clusters.size () << std::endl;
  //get length by acessing the coordinates 
  
    if(clusters.size() == 2)
    {
        //push cluster sizes into a vector. Sort big to small
        for(int i =0;  i<clusters.size(); i++)
        {
            cluster_sizes.push_back(clusters[i].indices.size());
        }
        sort(cluster_sizes.begin(), cluster_sizes.end(), greater<int>());
        
        for(int x = 0; x<2 ; x++)
        {
            if(clusters[x].indices.size() == cluster_sizes[0])
            {
                for(int j = 0; j < clusters[x].indices.size () ; j++)
                {
                    cloud->points.at(clusters.at(x).indices.at(j)).r = 0;
                    cloud->points.at(clusters.at(x).indices.at(j)).g = 0;
                    cloud->points.at(clusters.at(x).indices.at(j)).b = 255;
                }
            }
            if(clusters[x].indices.size() == cluster_sizes[1])
            {
                for(int j = 0; j < clusters[x].indices.size () ; j++)
                {
                    cloud->points.at(clusters.at(x).indices.at(j)).r = 0;
                    cloud->points.at(clusters.at(x).indices.at(j)).g = 255;
                    cloud->points.at(clusters.at(x).indices.at(j)).b = 0;
                }
            }
        }
    }
    if(clusters.size() == 3)
    {
        for(int i =0;  i<clusters.size(); i++)
        {
            cluster_sizes.push_back(clusters[i].indices.size());
        }
        sort(cluster_sizes.begin(), cluster_sizes.end(), greater<int>());
        
        for(int x = 0; x<3 ; x++)
        {
            if(clusters[x].indices.size() == cluster_sizes[0])
            {
                for(int j = 0; j < clusters[x].indices.size () ; j++)
                {
                    cloud->points.at(clusters.at(x).indices.at(j)).r = 0;
                    cloud->points.at(clusters.at(x).indices.at(j)).g = 0;
                    cloud->points.at(clusters.at(x).indices.at(j)).b = 255;
                }
            }
            if(clusters[x].indices.size() == cluster_sizes[1])
            {
                for(int j = 0; j < clusters[x].indices.size () ; j++)
                {
                    cloud->points.at(clusters.at(x).indices.at(j)).r = 0;
                    cloud->points.at(clusters.at(x).indices.at(j)).g = 255;
                    cloud->points.at(clusters.at(x).indices.at(j)).b = 0;
                }
            }
            if(clusters[x].indices.size() == cluster_sizes[2])
            {
                for(int j = 0; j < clusters[x].indices.size () ; j++)
                {
                    cloud->points.at(clusters.at(x).indices.at(j)).r = 255;
                    cloud->points.at(clusters.at(x).indices.at(j)).g = 0;
                    cloud->points.at(clusters.at(x).indices.at(j)).b = 0;
                }
            }
        }
    }
    if(clusters.size() == 4)
    {   
        //for loop of clusters[x].size() AND check color to find smallest and larggest point. use 'h' for finding smallest point. closest to negative infinity
        /*std::cout << "Cluster 1:  " << clusters[0].indices.size()<< " points." << std::endl;
        std::cout << "Cluster 2:  " << clusters[1].indices.size() << " points." << std::endl;
        std::cout << "Cluster 3:  " << clusters[2].indices.size() << " points." << std::endl;
        std::cout << "Cluster 4:  " << clusters[3].indices.size() << " points." << std::endl;*/
        for(int i =0;  i<clusters.size(); i++)
        {
            cluster_sizes.push_back(clusters[i].indices.size());
        }
        sort(cluster_sizes.begin(), cluster_sizes.end(), greater<int>());
        /*for(int i =0;  i<clusters.size(); i++)
        {
            std::cout<<"SizesX: "<<cluster_sizes[i]<<std::endl;
        }*/
        
        for(int x = 0; x<4 ; x++)
        {
            if(clusters[x].indices.size() == cluster_sizes[0])
            {
                for(int j = 0; j < clusters[x].indices.size () ; j++)
                {
                    cloud->points.at(clusters.at(x).indices.at(j)).r = 0;
                    cloud->points.at(clusters.at(x).indices.at(j)).g = 0;
                    cloud->points.at(clusters.at(x).indices.at(j)).b = 255;
                }
            }
            if(clusters[x].indices.size() == cluster_sizes[1])
            {
                for(int j = 0; j < clusters[x].indices.size () ; j++)
                {
                    cloud->points.at(clusters.at(x).indices.at(j)).r = 0;
                    cloud->points.at(clusters.at(x).indices.at(j)).g = 255;
                    cloud->points.at(clusters.at(x).indices.at(j)).b = 0;
                }
            }
            if(clusters[x].indices.size() == cluster_sizes[2])
            {
                for(int j = 0; j < clusters[x].indices.size () ; j++)
                {
                    cloud->points.at(clusters.at(x).indices.at(j)).r = 255;
                    cloud->points.at(clusters.at(x).indices.at(j)).g = 0;
                    cloud->points.at(clusters.at(x).indices.at(j)).b = 0;
                }
            }
            if(clusters[x].indices.size() == cluster_sizes[3])
            {
                for(int j = 0; j < clusters[x].indices.size () ; j++)
                {
                    cloud->points.at(clusters.at(x).indices.at(j)).r = 0;
                    cloud->points.at(clusters.at(x).indices.at(j)).g = 0;
                    cloud->points.at(clusters.at(x).indices.at(j)).b = 255;
                }
            }
        }
    }

    //segment the plane to get rid of table
    const float distanceThreshold = 0.0162;
    const int maxIterations =5000;
    pcl::PointIndices::Ptr inliers(new pcl::PointIndices);
    //std::cout << " cloud Points: " << cloud->points.size() << std::endl;
    segmentPlane(cloud, inliers, distanceThreshold, maxIterations);
    pcl::PointCloud<pcl::PointXYZRGBA>::Ptr cloudFiltered(new pcl::PointCloud<pcl::PointXYZRGBA>);
    removePoints(cloud, cloudFiltered, inliers);
    //std::cout << " cloudFiltered Points (removed table Plane): " << cloudFiltered->points.size() << std::endl;

    //run cloud through a voxel grid filter in order to get measurments easier
    //should not have the table present at this point
    //const float voxelSize = 0.0025;
    const float voxelSize = 0.01;
    pcl::PointCloud<pcl::PointXYZRGBA>::Ptr cloudFiltered2(new pcl::PointCloud<pcl::PointXYZRGBA>);
    pcl::VoxelGrid<pcl::PointXYZRGBA> voxFilter;
    voxFilter.setInputCloud(cloudFiltered);
    voxFilter.setLeafSize(static_cast<float>(voxelSize), static_cast<float>(voxelSize), static_cast<float>(voxelSize));
    voxFilter.filter(*cloudFiltered2);
    //std::cout << "Points before downsampling: " << cloud->points.size() << std::endl;
    //std::cout << "Points after downsampling: " << cloudFiltered2->points.size() << std::endl;

    //Vox filter WITH table
    pcl::PointCloud<pcl::PointXYZRGBA>::Ptr cloudFiltered3(new pcl::PointCloud<pcl::PointXYZRGBA>);
    pcl::VoxelGrid<pcl::PointXYZRGBA> voxFilter2;
    voxFilter.setInputCloud(cloud);
    voxFilter.setLeafSize(static_cast<float>(voxelSize), static_cast<float>(voxelSize), static_cast<float>(voxelSize));
    voxFilter.filter(*cloudFiltered3);

    //Get the length and width of each box
    //use the color as a conditional in order to not mix up the boxes
    int greenPoints = 0;
    int redPoints = 0;
    int bluePoints = 0;
    std::vector<float> xValues_Green;
    std::vector<float> xValues_Red;
    std::vector<float> yValues_Green;
    std::vector<float> yValues_Red;
    std::vector<float> zValues_Green;
    std::vector<float> zValues_Red;

    std::vector<float> zValues_Blue;
    float zAvg_Blue;
    float zAvg_Green;
    float zAvg_Red;

    for(int x=0; x<cloudFiltered2->points.size(); x++)
    {
        if(cloudFiltered2->points.at(x).g == 255 || cloudFiltered2->points.at(x).g > 200)
        {
            greenPoints++;
            xValues_Green.push_back(cloudFiltered2->points.at(x).x);
            yValues_Green.push_back(cloudFiltered2->points.at(x).y);
            zValues_Green.push_back(cloudFiltered2->points.at(x).z);
        }
        if(cloudFiltered2->points.at(x).r == 255 || cloudFiltered2->points.at(x).r > 200)
        {
            redPoints++;
            xValues_Red.push_back(cloudFiltered2->points.at(x).x);
            yValues_Red.push_back(cloudFiltered2->points.at(x).y);
            zValues_Red.push_back(cloudFiltered2->points.at(x).z);
        }
    }

    //get tabel z-Axis values seperately
    for(int x=0; x<cloudFiltered3->points.size(); x++)
    {
        if(cloudFiltered3->points.at(x).b == 255 || cloudFiltered3->points.at(x).b > 200)
        {
            zValues_Blue.push_back(cloudFiltered3->points.at(x).z);
            bluePoints++;
        }
    }

    

    //find top and bottom corners for tilted boxes
    /*int index=0;
    int index2=0;
    float max = *max_element(yValues_Green.begin(), yValues_Green.end());
    float min = *min_element(yValues_Green.begin(), yValues_Green.end());

    auto it = find(yValues_Green.begin(), yValues_Green.end(), min);
    // If element was found
    if (it != yValues_Green.end()) 
    {
        index = it - yValues_Green.begin();
        //cout << index << endl;
    }
    else 
    {
        cout << "-1" << endl;
    }

    //TODO
    auto it2 = find(yValues_Green.begin(), yValues_Green.end(), max);
    // If element was found
    if (it2 != yValues_Green.end()) 
    {
        index2 = it2 - yValues_Green.begin();
        //cout << index << endl;
    }
    else 
    {
        cout << "-1" << endl;
    }

    int index3=0;
    int index4=0;
    float max2 = *max_element(xValues_Green.begin(), xValues_Green.end());
    float min2 = *min_element(xValues_Green.begin(), xValues_Green.end());

    if (it != xValues_Green.end()) 
    {
        index3 = it - yValues_Green.begin();
        //cout << index << endl;
    }
    else 
    {
        cout << "-1" << endl;
    }

    auto it4 = find(xValues_Green.begin(), xValues_Green.end(), max2);
    // If element was found
    if (it4 != yValues_Green.end()) 
    {
        index4 = it4 - xValues_Green.begin();
        //cout << index << endl;
    }
    else 
    {
        cout << "-1" << endl;
    }

    //lefttmost corner
    float greenLeftmostCornerX = max2;
    float greenLeftmostCornerY = yValues_Green.at(index3);

    //rightmost corner
    float greenRightmostCornerX = min2;
    float greenRightmostCornerY = yValues_Green.at(index4);

    //top corner
    float greenBottomCornerX = xValues_Green.at(index);
    float greenBottomCornerY = min;

    //bottom corner
    float greenTopCornerX = xValues_Green.at(index2);
    float greenTopCornerY = max;
    */

    /*std::cout<<"Bottom Point: ("<<greenBottomCornerX<<","<<greenBottomCornerY<<")"<<std::endl;
    std::cout<<"Top Point: ("<<greenTopCornerX<<","<<greenTopCornerY<<")"<<std::endl;

    std::cout<<"Rightmost Point: ("<<greenRightmostCornerX<<","<<greenRightmostCornerY<<")"<<std::endl;
    std::cout<<"Leftmost Point: ("<<greenLeftmostCornerX<<","<<greenLeftmostCornerY<<")"<<std::endl;*/

    //LENGTH==Longest side, WIDTH==shortest Side , HEIGHT==zAxis
    //if red overlaps with another color, it will not be within the vector; causes inaccuracy
    sort(xValues_Green.begin(), xValues_Green.end(), greater<float>());
    sort(yValues_Green.begin(), yValues_Green.end(), greater<float>());
    sort(zValues_Green.begin(), zValues_Green.end(), greater<float>());

    sort(xValues_Red.begin(), xValues_Red.end(), greater<float>());
    sort(yValues_Red.begin(), yValues_Red.end(), greater<float>());
    sort(zValues_Red.begin(), zValues_Red.end(), greater<float>());

    for(int y = 0 ; y<zValues_Blue.size() ; y++)
    {
        zAvg_Blue = zAvg_Blue + zValues_Blue[y];
    }
    //only get the top half of points as some are "droopin" over the edge
    for(int y = 0 ; y<zValues_Red.size()/2  ; y++)
    {
        zAvg_Red = zAvg_Red + zValues_Red[y];
    }
    for(int y = 0 ; y<zValues_Green.size()/2 ; y++)
    {
        zAvg_Green = zAvg_Green + zValues_Green[y];
    }

    zAvg_Blue = zAvg_Blue / zValues_Blue.size();
    zAvg_Red = zAvg_Red / zValues_Red.size();
    zAvg_Green = zAvg_Green / zValues_Green.size();
    


    float redBoxLength=0;
    float redBoxWidth=0;
    float greenBoxLength=0;
    float greenBoxWidth=0;

    //make sure the longest side is the length
    if(clusters.size() == 2)
    {
        greenBoxLength = xValues_Green[0] - xValues_Green[greenPoints-1];
        greenBoxWidth = yValues_Green[0] - yValues_Green[greenPoints-1];

        std::cout<<"LENGTH, WIDTH, HEIGHT"<<std::endl;

        if(zAvg_Blue>=0)
        {
            std::cout<<"BOX 1: ("<<greenBoxLength<<","<<greenBoxWidth<<","<<zAvg_Green-zAvg_Blue<<")"<<std::endl;
        }
        if(zAvg_Blue<=0)
        {
            std::cout<<"BOX 1: ("<<greenBoxLength<<","<<greenBoxWidth<<","<<zAvg_Green + abs(zAvg_Blue)<<")"<<std::endl;
        }
        
    }
    
    if(clusters.size() == 3 || clusters.size() == 4)
    {
        if(( xValues_Red[0] + abs(xValues_Red[redPoints-1]) > yValues_Red[0] + abs(yValues_Red[redPoints-1])) && yValues_Red[redPoints-1] < 0 && xValues_Red[redPoints-1] < 0)
        {
            redBoxLength = xValues_Red[0]-xValues_Red[redPoints-1];
            redBoxWidth = yValues_Red[0]-yValues_Red[redPoints-1];
        }
        if(( xValues_Red[0] + abs(xValues_Red[redPoints-1]) > yValues_Red[0] - abs(yValues_Red[redPoints-1])) && yValues_Red[redPoints-1] > 0 && xValues_Red[redPoints-1] < 0)
        {
            redBoxLength = xValues_Red[0]-xValues_Red[redPoints-1];
            redBoxWidth = yValues_Red[0]-yValues_Red[redPoints-1];
        }
        if(( xValues_Red[0] - abs(xValues_Red[redPoints-1]) > yValues_Red[0] + abs(yValues_Red[redPoints-1])) && yValues_Red[redPoints-1] < 0 && xValues_Red[redPoints-1] > 0)
        {
            redBoxLength = xValues_Red[0]-xValues_Red[redPoints-1];
            redBoxWidth = yValues_Red[0]-yValues_Red[redPoints-1];
        }
        if(( xValues_Red[0] - abs(xValues_Red[redPoints-1]) > yValues_Red[0] - abs(yValues_Red[redPoints-1])) && yValues_Red[redPoints-1] > 0 && xValues_Red[redPoints-1] > 0)
        {
            redBoxLength = xValues_Red[0]-xValues_Red[redPoints-1];
            redBoxWidth = yValues_Red[0]-yValues_Red[redPoints-1];
        }
        
        //XXXXXXX
        if(( xValues_Red[0] + abs(xValues_Red[redPoints-1]) < yValues_Red[0] + abs(yValues_Red[redPoints-1])) && yValues_Red[redPoints-1] < 0 && xValues_Red[redPoints-1] < 0)
        {
            redBoxWidth = xValues_Red[0]-xValues_Red[redPoints-1];
            redBoxLength = yValues_Red[0]-yValues_Red[redPoints-1];
        }
        if(( xValues_Red[0] + abs(xValues_Red[redPoints-1]) < yValues_Red[0] - abs(yValues_Red[redPoints-1])) && yValues_Red[redPoints-1] > 0 && xValues_Red[redPoints-1] < 0)
        {
            redBoxWidth = xValues_Red[0]-xValues_Red[redPoints-1];
            redBoxLength= yValues_Red[0]-yValues_Red[redPoints-1];
        }
        if(( xValues_Red[0] - abs(xValues_Red[redPoints-1]) < yValues_Red[0] + abs(yValues_Red[redPoints-1])) && yValues_Red[redPoints-1] < 0 && xValues_Red[redPoints-1] > 0)
        {
            redBoxWidth = xValues_Red[0]-xValues_Red[redPoints-1];
            redBoxLength = yValues_Red[0]-yValues_Red[redPoints-1];
        }
        if(( xValues_Red[0] - abs(xValues_Red[redPoints-1]) < yValues_Red[0] - abs(yValues_Red[redPoints-1])) && yValues_Red[redPoints-1] > 0 && xValues_Red[redPoints-1] > 0)
        {
            redBoxWidth = xValues_Red[0]-xValues_Red[redPoints-1];
            redBoxLength = yValues_Red[0]-yValues_Red[redPoints-1];
        }


        if(( xValues_Green[0] + abs(xValues_Green[greenPoints-1]) > yValues_Green[0] + abs(yValues_Green[greenPoints-1])) && yValues_Green[greenPoints-1] < 0 && xValues_Green[greenPoints-1] < 0)
        {
            greenBoxLength = xValues_Green[0]-xValues_Green[greenPoints-1];
            greenBoxWidth = yValues_Green[0]-yValues_Green[greenPoints-1];
        }
        if(( xValues_Green[0] + abs(xValues_Green[greenPoints-1]) > yValues_Green[0] - abs(yValues_Green[greenPoints-1])) && yValues_Green[greenPoints-1] > 0 && xValues_Green[greenPoints-1] < 0)
        {
            greenBoxLength = xValues_Green[0]-xValues_Green[greenPoints-1];
            greenBoxWidth = yValues_Green[0]-yValues_Green[greenPoints-1];
        }
        if(( xValues_Green[0] - abs(xValues_Green[greenPoints-1]) > yValues_Green[0] + abs(yValues_Green[greenPoints-1])) && yValues_Green[greenPoints-1] < 0 && xValues_Green[greenPoints-1] > 0)
        {
            greenBoxLength = xValues_Green[0]-xValues_Green[greenPoints-1];
            greenBoxWidth = yValues_Green[0]-yValues_Green[greenPoints-1];
        }
        if(( xValues_Green[0] - abs(xValues_Green[greenPoints-1]) > yValues_Green[0] - abs(yValues_Green[greenPoints-1])) && yValues_Green[greenPoints-1] > 0 && xValues_Green[greenPoints-1] > 0)
        {
            greenBoxLength = xValues_Green[0]-xValues_Green[greenPoints-1];
            greenBoxWidth = yValues_Green[0]-yValues_Green[greenPoints-1];
        }
        /////////////
        if(( xValues_Green[0] + abs(xValues_Green[greenPoints-1]) < yValues_Green[0] + abs(yValues_Green[greenPoints-1])) && yValues_Green[greenPoints-1] < 0 && xValues_Green[greenPoints-1] < 0)
        {
            greenBoxWidth = xValues_Green[0]-xValues_Green[greenPoints-1];
            greenBoxLength = yValues_Green[0]-yValues_Green[greenPoints-1];
        }
        if(( xValues_Green[0] + abs(xValues_Green[greenPoints-1]) < yValues_Green[0] - abs(yValues_Green[greenPoints-1])) && yValues_Green[greenPoints-1] > 0 && xValues_Green[greenPoints-1] < 0)
        {
            greenBoxWidth = xValues_Green[0]-xValues_Green[greenPoints-1];
            greenBoxLength = yValues_Green[0]-yValues_Green[greenPoints-1];
        }
        if(( xValues_Green[0] - abs(xValues_Green[greenPoints-1]) < yValues_Green[0] + abs(yValues_Green[greenPoints-1])) && yValues_Green[greenPoints-1] < 0 && xValues_Green[greenPoints-1] > 0)
        {
            greenBoxWidth = xValues_Green[0]-xValues_Green[greenPoints-1];
            greenBoxLength = yValues_Green[0]-yValues_Green[greenPoints-1];
        }
        if(( xValues_Green[0] - abs(xValues_Green[greenPoints-1]) < yValues_Green[0] - abs(yValues_Green[greenPoints-1])) && yValues_Green[greenPoints-1] > 0 && xValues_Green[greenPoints-1] > 0)
        {
            greenBoxWidth = xValues_Green[0]-xValues_Green[greenPoints-1];
            greenBoxLength = yValues_Green[0]-yValues_Green[greenPoints-1];
        }

        std::cout<<" LENGTH, WIDTH, HEIGHT"<<std::endl;
        if(zAvg_Blue>0)
        {
            std::cout<<"BOX 1: ("<<greenBoxLength<<","<<greenBoxWidth<<","<<zAvg_Green - zAvg_Blue<<")"<<std::endl;
        }
        if(zAvg_Blue<0)
        {
            std::cout<<"BOX 1: ("<<greenBoxLength<<","<<greenBoxWidth<<","<<zAvg_Green + abs(zAvg_Blue)<<")"<<std::endl;
        }

        if(zAvg_Blue>0)
        {
            std::cout<<"BOX 2: ("<<redBoxLength<<","<<redBoxWidth<<","<<zAvg_Red - zAvg_Blue<<")"<<std::endl;
        }
        if(zAvg_Blue<0)
        {
            std::cout<<"BOX 2: ("<<redBoxLength<<","<<redBoxWidth<<","<<zAvg_Red + abs(zAvg_Blue)<<")"<<std::endl;
        }
        
    }

  /*pcl::visualization::CloudViewer viewer ("VIEW");
  viewer.showCloud(cloud);
  while (!viewer.wasStopped ()) {}*/
    CloudVisualizer CV("Rendering Window");

    // render the scene
    CV.addCloud(cloud);
    //CV.addCloud(cloudFiltered3);
    //CV.addCloud(cloudFiltered);
    CV.addCoordinateFrame(cloud->sensor_origin_, cloud->sensor_orientation_);

    // register mouse and keyboard event callbacks
    CV.registerPointPickingCallback(pointPickingCallback, cloud);
    CV.registerKeyboardCallback(keyboardCallback);

    // enter visualization loop
    while(CV.isRunning())
    {
        CV.spin(100);
    }
  
  return (0);
}