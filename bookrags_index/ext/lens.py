from ..ext.definitions import ProductType
import re
from requests.sessions import Session
from ..ext.product import Product
from typing import List


class Lens:
    """
    Special product type that contains references to all resources
    """

    def __init__(self, session: Session, link: str) -> None:
        self._session = session
        self._link = link
        self._content = session.get(link).text

    def get_link(self) -> str:
        return self._link

    def get_title(self) -> str:
        page_title = re.search('<title>(.*?)</title>', self._content)
        return page_title.group(1)

    def get_study_pack(self) -> List[Product]:
        """
        Returns all the pages for a study pack
        """
        ret = []
        ret.extend(self.get_study_guides())
        ret.extend(self.get_encyclopedias())
        ret.extend(self.get_ebooks())
        ret.extend(self.get_biographies())
        ret.extend(self.get_essays())

        return ret

    def _extract_links(self, expression: str, type: ProductType) -> List[Product]:
        ret = []
        block_code = re.search(expression, self._content, flags=re.DOTALL)
        if not block_code:
            return ret
        links = re.findall("href='(.*?)'", block_code.group())
        existing = {}
        for i in links:
            if i not in existing:
                existing[i] = True
            else:
                continue
            ret.append(Product(self._session, i, type))
        return ret

    def get_lesson_plans(self) -> List[Product]:
        ret = self._extract_links(
            '<!-- BEGIN LESSON PLAN CONTENTS BLOCK -->(.*?)<!-- END LESSON PLAN CONTENTS BLOCK -->',
            ProductType.LESSON_PLAN
        )
        if len(ret) > 0:
            return [ret[0]]
        else:
            return []


    def get_study_guides(self) -> List[Product]:
        """
        Return all study guide Product products
        """
        ret = self._extract_links(
            '<!-- BEGIN STUDY GUIDE BLOCK -->(.*?)<!-- END STUDY GUIDE BLOCK -->',
            ProductType.STUDY_GUIDE
        )

        if len(ret) > 0:
            return [ret[0]]
        else:
            return []

    def get_encyclopedias(self) -> List[Product]:
        """
        Return all encyclopedia / gale products
        """
        return self._extract_links(
            '<!-- BEGIN ENCYCLOPEDIA BLOCK -->(.*?)<!-- END ENCYCLOPEDIA BLOCK -->',
            ProductType.ENCYCLOPEDIA
        )

    def get_ebooks(self) -> List[Product]:
        """
        Get all ebook products
        """
        return self._extract_links(
            '<!-- BEGIN EBOOKS BLOCK -->(.*?)<!-- #topicEBooksBlock -->',
            ProductType.EBOOK
        )

    def get_biographies(self) -> List[Product]:
        """
        Get all biography products
        """
        return self._extract_links(
            '<!-- BEGIN BIOGRAPHY BLOCK -->(.*?)<!-- END BIOGRAPHY BLOCK -->',
            ProductType.BIOGRAPHY
        )

    def get_essays(self) -> List[Product]:
        """
        Get all essay products
        """
        return self._extract_links(
            '<!-- BEGIN ESSAYS BLOCK -->(.*?)<!-- END ESSAYS BLOCK -->',
            ProductType.ESSAY
        )

    def get_notes(self) -> List[Product]:
        """
        Not supported, they are included in the study guide
        """
        return []
