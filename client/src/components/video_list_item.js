import React from 'react';
var axios = require('axios');

function onVideoClick(video) {
    axios.post('/queue', {
        id: video.id.videoId,
        title: video.snippet.title
    })
    .then(function (response) {
        console.log(response);
        Materialize.toast(response.data, 3000, 'rounded')
    })
    .catch(function (error) {
        console.log(error);
    });

    return "ok";
};


const VideoListItem = ({video}) => {
  const imageUrl = video.snippet.thumbnails.default.url;

  return (
<div>
 <div className="row">
    <div className="col s12">
      <div className="card">
        <div className="card-image">
          <img src={imageUrl}/>
          <a onClick={() => onVideoClick(video)} className="btn-floating halfway-fab waves-effect waves-light red btn-large"><i className="material-icons">add</i></a>
        </div>
        <div className="card-content">
          <p>{video.snippet.title}</p>
        </div>
          <div className="card-action">
              <p style={{color: 'gray'}}>{video.snippet.channelTitle}</p>
            </div>

      </div>
    </div>
  </div>


</div>

  );
}

export default VideoListItem;
