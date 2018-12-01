import React from "react"
import {Query, Mutation} from "react-apollo"
import gql from "graphql-tag"
import LotChart from "./LotChart"
import {GET_SECTORS_QUERY} from'./GraphQL'


const SectorQuery = () => (
    <Query
        query={GET_SECTORS_QUERY}
    >
    {({loading, error, data, refetch}) => {
        if (loading) return (<p>Loading...</p>)
        if (error) return (<p>Error :</p>)

        return (
                    <div>
                        <LotChart data = {data.allSectors} width= {1600} height={800} onRefetch={()=> refetch()}/>
                    </div>
        )

    }}
    </Query>
)


export default SectorQuery