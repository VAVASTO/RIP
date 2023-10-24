import { FC, useState} from 'react'
import { Card, Col, Row, Button, Spinner } from 'react-bootstrap'
import './ITunesPage.css'

interface ITunesMusic {
    wrapperType: string
    artworkUrl100: string
    artistName: string
    collectionCensoredName: string
    trackViewUrl: string
}

interface ITunesResult {
    resultCount: number
    results: ITunesMusic[]
}

const getMusicByName = async (name = ''): Promise<ITunesResult> =>{
    return fetch(`https://itunes.apple.com/search?term=${name}`)
        .then((response) => response.json())
        .catch(()=> ({ resultCount:0, results:[] }))
}

const ITunesPage: FC = () => {
    const [searchValue, setSearchValue] = useState('')

    const [loading, setLoading] = useState(false)

    const [music, setMusic] = useState<ITunesMusic[]>([])

    const handleSearch = async () =>{
        await setLoading(true)
        const { results } = await getMusicByName(searchValue)
        await setMusic(results.filter(item => item.wrapperType === "track"))
        await setLoading(false)
    }

    return (
        <div className={`container ${loading && 'containerLoading'}`}>
            {loading && <div className="loadingBg"><Spinner animation="border"/></div>}

            <div className="inputField">
                <input value={searchValue} onChange={(event => setSearchValue(event.target.value))}/>
                <Button disabled={loading} onClick={handleSearch}>Искать</Button>
            </div>

            {!music.length && <div>
                <h1>К сожалению, пока ничего не найдено :(</h1>
            </div>}

            <Row xs={4} md={4} className="g-4">
                {music.map((item, index)=> (
                    <Col >
                        <Card key={index} className="card">
                            <Card.Img className="cardImage" variant="top" src={item.artworkUrl100} height={100} width={100}  />
                            <Card.Body>
                            
                            <div className="textStyle">
                                <Card.Title>{item.artistName}</Card.Title>
                            </div>

                            <div className="textStyle">
                                <Card.Text>
                                    {item.collectionCensoredName}
                                </Card.Text>
                            </div>

                            <Button className="cardButton" href={item.trackViewUrl} target="_blank" variant="primary">Открыть в ITunes</Button>
                            </Card.Body>
                        </Card>
                    </Col>
                ))}
            </Row>
        </div>
    )
}

export default ITunesPage