import gql from "graphql-tag"

const UPDATE_SECTOR_LOCATION = gql`
    mutation UpdateSector($id: Int! $xIndex: Int! $yIndex: Int!){
        updateSector(id: $id, xIndex: $xIndex, yIndex: $yIndex){
            id
            xIndex
            yIndex
        }
    }
`

const GET_SECTORS_QUERY = gql`
    {
        allSectors {
            id
            xIndex
            yIndex
            sectorSpots{
                id
                spot{
                    id
                    active
                    full
                }
                imageCoordinates{
                    id
                    bottom
                    left
                    right
                    top
                }
            }
        }
    }`

export {GET_SECTORS_QUERY, UPDATE_SECTOR_LOCATION}