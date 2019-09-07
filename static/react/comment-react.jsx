"use strict";

class Comment extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            items:[],
            isLoaded: false,
        }
    }

    componentDidMount() {

        fetch('/photos/comments.json')
        .then(res => res.json())
        .then(json => {
            this.setState({
                isLoaded: true,
                items: json,
            })
            
        });

    }
  
    render() {

        var { isLoaded, items } = this.state;

        const result = items.filter(item => item.photo_id == this.props.photoId)

        const comments = result.map(item => (

                        <li key={item.comment_id}>
                            <div class="commenterImage">
                                <i class="fas fa-user-circle fa-lg"></i>
                            </div>
                            <div class="commentText">
                                { item.comment }
                            </div>
                        </li>

                        ))

        return (
            <div className="commentNodes">

                <div className="titleBox">
                    <label>Comments</label>
                </div>
                <div className="actionBox">
                    <ul className="commentList" id="commentId">
                        <li>
                            <div className="commentText">
                                { comments }
                            </div>
                        </li>
                    </ul>
                </div>
            </div>

            );
    }
}

const commentNodes = document.querySelectorAll(".commentNodes")

for (let commentNode of commentNodes) {

    const photo_id = $(commentNode).data('photo-id')

    ReactDOM.render(<Comment photoId={photo_id}/>, commentNode);
}






