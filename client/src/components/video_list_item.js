import React from 'react';
var axios = require('axios');

function onVideoClick(video) {
    console.log(video);
    axios.post('/queue', {
        id: video.id.videoId,
        title: video.snippet.title
    })
    .then(function (response) {
        console.log(response);
    })
    .catch(function (error) {
        console.log(error);
    });

    return "ok";
};


const VideoListItem = ({video, onVideoSelect}) => {
  const imageUrl = video.snippet.thumbnails.default.url;

  return (
  <li onClick={() => onVideoClick(video)} className="list-group-item">
    <div className="video-list media">
      <div className="media-left">
        <img className="media-object" src={imageUrl} />
      </div>
      <div className="media-body">
        <div className="media-heading">{video.snippet.title}</div>
        <div className="media-heading">{video.snippet.channelTitle}</div>
      </div>
    </div>
  </li>
  );
}

export default VideoListItem;
