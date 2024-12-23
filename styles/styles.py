# styles/styles.py

def get_thumbnail_css():
    return """
        <style>
        /* Container styling for YouTube thumbnail */
        .thumbnail-container {
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
            margin: 0 auto;
            width: 100%; /* Responsive width */
            max-width: 640px; /* Maximum width for larger screens */
            height: 0; /* Set height to zero to use padding for aspect ratio */
            padding-bottom: 56.25%; /* 16:9 Aspect Ratio (360/640 = 0.5625) */
            position: relative; /* Position for absolute children */
            border: 2px solid #e6e6e6; /* Light gray border */
            border-radius: 8px; /* Corner radius similar to YouTube */
            background-color: #ffffff; /* Background color for consistency */
        }

        /* Image styling to remove black bars */
        .thumbnail-container img {
            position: absolute; /* Positioning the image absolutely */
            top: 0;
            left: 0;
            width: 100%; /* Ensures image fills the container */
            height: 100%; /* Ensures image fills the container */
            object-fit: cover; /* Ensures image covers the entire container */
            border-radius: 8px; /* Match border radius to container */
        }
        </style>
    """

get_titleCenter_css = """
    <style>
    .centered-title {
        text-align: center;
    }
    </style>
    """


