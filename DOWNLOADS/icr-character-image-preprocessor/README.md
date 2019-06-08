The Open ICR Image Pre-processor
================================
An Python script used to pre-process images of individual handwritten characters to increase OCR/ICR accuracy
Part of the Open ICR Project - http://opensource.newmediaist.com/open-source-icr.html
          <p>The purpose of this image pre-processor is to "sanitize and standardize" the input image as much as possible to prepare it for the recognition engine. The image preprocessor has the following dependencies:<BR />
            <ul>
              <li>Python & the following Python Plugins:</li>
              <li><a href="http://opencv.willowgarage.com/wiki/">OpenCV</a></li>
              <li><a href="http://www.numpy.org/">NumPy</a></li>
              <li><a href="http://www.scipy.org">sciPy</a></li>
              <li><a href="https://github.com/yati-sagade/zhang-suen-thinning">zhangsuen</a></li>
            </ul>
            The following is a short summary of the different modifications the image pre-processor makes to the image:
          <ol>
            <li>Remove borders around the character (i.e. from imperfect character extraction)</li>
            <li>Median filtering is applied to remove salt and pepper type noise</li>
            <li>Character image is cropped down to borders of written character</li>
            <li>Character image is scaled to a standard set of dimensions</li>
            <li>Character image is thinned using Zhang Suen algo</li>
            <li>White space padding added around the image to prepare for next stage</li>
            <li>Erosion is added to the character image to join small gaps</li>
          </ol>
          <h3>Usage</h3>
          <p>
          <strong>python preprocessor.py -o original.png-d ~path_for_output\filename.png</strong>
          </p>
          <p>Code licensed under <a href="http://www.apache.org/licenses/LICENSE-2.0" target="_blank">Apache License v2.0</a></p>