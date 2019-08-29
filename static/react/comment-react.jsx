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

        return (
            <div class="commentNodes">

                <ul>
                    {items.map(item => (

                        <li key={item.photo_id}>
                            {item.comment}
                        </li>

                        ))}
                </ul>
            </div>

            );
    }
}

const commentNodes = document.querySelectorAll(".commentNodes")

for (let commentNode of commentNodes) {

    ReactDOM.render(
    <Comment/>,
    commentNode);
        }





