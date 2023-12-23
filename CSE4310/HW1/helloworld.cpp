
#include <iostream>
#include <string>
#include "opencv2/opencv.hpp"
#include "opencv2/core/core.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"

static void clickCallback(int event, int x, int y, int flags, void* param);//added int event 2


int b = 255;
int g = 255;
int r = 255;
int right_click=1;




cv::Mat pencil_image;



cv::Point p1, p2;
cv::Rect area;
int is_cropped=0;

//use right click to toggle between tools

static void clickCallback(int event, int x, int y, int flags, void* param)
{
    cv::Mat imageIn = *(cv::Mat *)param;
    cv::Mat clonedImage=imageIn.clone();
    int reset_toggle=0;
    int is_cropped=0;


    if(event == cv::EVENT_RBUTTONDOWN)//toggle function
    {
        right_click++;
        if(right_click==1)
        {
            std::cout << "EYEDROPPER" << std::endl;
        }
        else if(right_click==2)
        {
            std::cout << "CROP" << std::endl;
        }
        else if(right_click==3)
        {
            std::cout << "PENCIL" << std::endl;
        }
        else if(right_click==4)
        {
            std::cout << "PAINT BUCKET" << std::endl;
        }
        else if(right_click==5)
        {
            std::cout << "RESET" << std::endl;
            right_click=0;

        }

    }

    if(event == cv::EVENT_LBUTTONDOWN && right_click==1) //eyedropper function
    {
        //std::cout << "EYEDROPPER" << std::endl;
        //std::cout << "LEFT CLICK (" << x << ", " << y << ")" << std::endl;
        b = clonedImage.at<cv::Vec3b>(y, x)[0];
        g = clonedImage.at<cv::Vec3b>(y, x)[1];
        r = clonedImage.at<cv::Vec3b>(y, x)[2];
        //pixel = imageIn.at<cv::Vec3b>(y, x);
        std::cout<<"COLOR UPDATED TO: ["<<b<<","<<g<<","<<r<<"]"<<std::endl;
    }

    if(right_click==2)//crop function
    {
        if(event==cv::EVENT_LBUTTONDOWN)
        {
            p1.x=x;
            p1.y=y;
        }
        if(event==cv::EVENT_LBUTTONUP)
        {
            p2.x=x;
            p2.y=y;

            area.height=abs(p2.y-p1.y);
            area.width=abs(p2.x-p1.x);
            if(p1.y>p2.y)
            {
                area.y=p2.y;
            }
            if(p1.y<p2.y)
            {
                area.y=p1.y;
            }
            if(p1.x>p2.x)
            {
                area.x=p2.x;
            }
            if(p1.x<p2.x)
            {
                area.x=p1.x;
            }
            cv::Mat newimage(imageIn,area);

            //imshow("New Image",newimage);

            if(area.height<50 || area.width<50)
            {
                std::cout<<"Area must be at least 50x50 pixels \n"<<std::endl;
            }
            else
            {
                is_cropped=1;
                cv::Rect area(p1,p2);
                cv::imshow("New",newimage);
                cv::waitKey();
                newimage=newimage(area).clone();
            }
        }
    }

    if(right_click==3)//Pencil Function
    {
        if(event==cv::EVENT_MOUSEMOVE)
        {
            cv::Vec3b &pixel=imageIn.at<cv::Vec3b>(y,x);
            pixel[0]=b;
            pixel[1]=g;
            pixel[2]=r;

            cv::imshow("New",imageIn);
            cv::waitKey();
        }
    }

    if(event == cv::EVENT_LBUTTONDOWN && right_click==4)//Paintbucket function
    {
        cv::Rect area;

		cv::floodFill(
			imageIn,
			cv::Point(x,y),
			cv::Scalar(b, g, r),
			&area,
			cv::Scalar(0,0,0),
			cv::Scalar(0,0,0),
			4
		);

		cv::imshow("New", imageIn);
        cv::waitKey();

    }
    if(event == cv::EVENT_LBUTTONDOWN && right_click==0)//Reset Function
    {
        cv::destroyWindow("New");
        clonedImage=imageIn.clone();
        cv::reloadImage();
    }

}

int main(int argc, char **argv)
{
    // open the input image
    std::string inputFileName = argv[1];
    cv::Mat imageIn;
    imageIn = cv::imread(inputFileName, cv::IMREAD_COLOR);

    // check for file error
    if(!imageIn.data)
    {
        std::cout << "Error while opening file " << inputFileName << std::endl;
        return 0;
    }

    // display the input image
    cv::imshow("imageIn", imageIn);
    cv::setMouseCallback("imageIn", clickCallback, &imageIn);
    cv::waitKey();
}
