import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Button from '@material-ui/core/Button';

const FollowButton = (props) => {
  const [following, setFollowing] = useState(false);

  useEffect(() => {
    let mounted = true;

    const checkIfFollowing = () => {
      axios({
        method: 'GET',
        url: 'http://localhost:5000/is_following',
        params: { following: props.uploader },
      }).then((response) => {
        console.log(response);
        if (response.data.result === true && mounted) {
          setFollowing(true);
        } else if (mounted) {
          setFollowing(false);
        }
      });
    };

    checkIfFollowing();

    return () => {
      mounted = false;
    };
  }, []);

  const handleFollowClicked = () => {
    const follow = () => {
      axios({
        method: 'POST',
        url: 'http://localhost:5000/follow',
        params: { to_follow: props.uploader },
      }).then((response) => {
        console.log(response);
        if (response.data.result === true) {
          setFollowing(true);
        } else {
          setFollowing(false);
        }
      });
    };

    const unfollow = () => {
      axios({
        method: 'POST',
        url: 'http://localhost:5000/unfollow',
        params: { following: props.uploader },
      }).then((response) => {
        console.log(response);
        if (response.data.result === true) {
          setFollowing(false);
        } else {
          setFollowing(true);
        }
      });
    };

    if (following) {
      unfollow();
    } else {
      follow();
    }
  };

  return (
    <React.Fragment>
      {following ? (
        <Button
          variant="contained"
          color="primary"
          style={{}}
          onClick={handleFollowClicked}
        >
          Following
        </Button>
      ) : (
        <Button
          variant="outlined"
          color="primary"
          style={{}}
          onClick={handleFollowClicked}
        >
          Follow
        </Button>
      )}
    </React.Fragment>
  );
};

export default FollowButton;
