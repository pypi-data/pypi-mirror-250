from typing import Optional
from sumatra_client.client import Client


class OptimizeClient(Client):
    def __init__(
        self,
        instance: Optional[str] = None,
        branch: Optional[str] = None,
        workspace: Optional[str] = None,
    ):
        super().__init__(
            instance=instance,
            branch=branch,
            workspace=workspace,
        )

    def create_audience(self, name, description, rule):
        query = """
            mutation CreateAudience($description: String, $name: String, $rule: JSON) {
                createAudience(description: $description, name: $name, rule: $rule) {
                    slug
                    description
                    name
                }
            }
        """
        ret = self._execute_graphql(
            query=query,
            variables={"name": name, "description": description, "rule": rule},
        )
        return ret["data"]["createAudience"]["slug"]

    def delete_audience(self, slug):
        query = """
            mutation DeleteAudience($slug: String!) {
                deleteAudience(slug: $slug) {
                    slug
                }
            }
        """
        ret = self._execute_graphql(
            query=query,
            variables={"slug": slug},
        )
        return ret["data"]["deleteAudience"]["slug"]

    def delete_optimization(self, id):
        query = """
            mutation DeleteOptimization($id: String!) {
                deleteOptimization(id: $id) {
                    id
                }
            }
        """
        ret = self._execute_graphql(
            query=query,
            variables={"id": id},
        )
        return ret["data"]["deleteOptimization"]["id"]

    def put_optimization(self, id, slug, name, description, rootPage):
        query = """
            mutation PutOptimization($id: String!, $slug: String, $name: String, $description: String, $rootPage: String) {
                putOptimization(id: $id, slug: $slug, name: $name, description: $description, rootPage: $rootPage) {
                    id
                    slug
                    name
                    description
                    rootPage
                }
            }
        """
        ret = self._execute_graphql(
            query=query,
            variables={
                "id": id,
                "slug": slug,
                "name": name,
                "description": description,
                "rootPage": rootPage,
            },
        )
        return ret["data"]["putOptimization"]

    def get_optimization(self, id):
        query = """
            query GetOptimization($id: String!) {
                optimization(id: $id) {
                    id
                    slug
                    name
                    description
                    rootPage
                    holdoutPercentage
                    goal {
                        type
                    }
                    experiences {
                        ...ExperienceParts
                    }
                }
            }

            fragment ExperienceParts on Experience {
                id
                name
                slug
                status
                experimentId
                audiences {
                    ...AudienceParts
                }
                variants {
                    ...VariantParts
                }
            }

            fragment AudienceParts on Audience {
                slug
                name
            }

            fragment VariantParts on Variant {
                name
                slug
                percentage
                overrides {
                    path
                    selector
                    type
                    value
                    xPath
                }
            }
        """
        ret = self._execute_graphql(
            query=query,
            variables={"id": id},
        )
        return ret["data"]["optimization"]

    def list_optimizations(self):
        query = """
                query ListOptimizations {
                    optimizations(first: 10) {
                        nodes {
                            id
                            name
                            slug
                            holdoutPercentage
                            rootPage
                        }
                    }
                }
            """
        ret = self._execute_graphql(
            query=query,
        )
        return ret["data"]["optimizations"]["nodes"]
