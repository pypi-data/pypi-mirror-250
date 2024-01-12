import io,traceback
from PIL import Image 

class ImageUtils:              

    @staticmethod
    def imgBytesCrop(sourceImageBytes, left_top_right_bottom):        
        """_summary_

        Parameters
        ----------
        sourceImageBytes : bytes
            source Image Bytes
        left_top_right_bottom : tuple
            crop range, like (0,0,1000,2000)

        Returns
        -------
        bytes
            cropped image bytes
        """
        img = Image.open(io.BytesIO(sourceImageBytes))
        
        format = img.format
        imgByteArr = io.BytesIO()
        img.crop(left_top_right_bottom).save(imgByteArr, format)            
        img_data = imgByteArr.getvalue()
        # with open(f'tmp12.{format}','wb') as f: f.write(img_data)
        return img_data
        
